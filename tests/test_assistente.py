import contextlib
import io
import unittest

import main
from energia.assistente import AssistenteEnergia, identificar_intencao, reais


class TestIntencoes(unittest.TestCase):
    def test_reconhece_perguntas_com_e_sem_acento(self):
        casos = {
            "Quanto meu chuveiro gasta?": "consumo",
            "dicas pra economizar": "habitos",
            "Vale a pena um aquecedor solar?": "solar_termico",
            "e painel solar fotovoltaico?": "fotovoltaica",
            "qual a MELHOR opção pra mim": "comparar",
            "moro de aluguel": "aluguel",
            "tenho direito a tarifa social?": "tarifa_social",
            "qual o impacto ambiental": "ambiental",
            "como você calculou isso?": "calculo",
            "quais as fontes": "fontes",
            "isso é garantido?": "limitacoes",
            "bom dia": "ajuda",
            # frases do teste de uso (docs/testes_usuarios.md) que antes caíam na ajuda
            "como baixar a conta?": "habitos",
            "tenho bolsa familia, pago luz?": "tarifa_social",
            "o que é kwh?": "kwh",
            "e se eu tomar banho de 10 minutos?": "simular",
            "minha casa tem 6 pessoas": "simular",
            "qual opção é mais barata?": "comparar",
            "isso polui?": "ambiental",
            "posso confiar nesses numeros?": "limitacoes",
            "qual a diferença entre aquecedor solar e painel solar?": "comparar",
            "energia solar por assinatura": "aluguel",
            # frases da simulação com personas (docs/testes_usuarios.md)
            "isso é certo?": "limitacoes",
            "quanto tempo pra pagar a placa": "fotovoltaica",
            "em quanto tempo se paga?": "comparar",
        }
        for pergunta, esperado in casos.items():
            with self.subTest(pergunta=pergunta):
                self.assertEqual(identificar_intencao(pergunta), esperado)


class TestRespostas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assistente = AssistenteEnergia()
        cls.cenario, cls.alts = cls.assistente.analise()

    def test_toda_resposta_traz_aviso_de_estimativa(self):
        for pergunta in ("chuveiro", "dicas", "aquecedor solar", "painel", "comparar", "aluguel",
                         "tarifa social", "ambiental", "calculou", "fontes", "garantido", ""):
            with self.subTest(pergunta=pergunta):
                self.assertIn("ESTIMATIVAS", self.assistente.responder(pergunta).formatar())

    def test_respostas_tecnicas_citam_fontes(self):
        for pergunta in ("chuveiro", "dicas", "aquecedor solar", "painel", "comparar", "ambiental"):
            with self.subTest(pergunta=pergunta):
                self.assertTrue(self.assistente.responder(pergunta).fontes)

    def test_numeros_da_resposta_sao_os_da_analise(self):
        texto = self.assistente.responder("comparar").texto
        for alt in self.alts:
            self.assertIn(reais(alt.economia_liquida_ano), texto)
        self.assertIn(reais(self.cenario.custo_chuveiro_ano), texto)

    def test_simulacao_rapida_recalcula_pela_pergunta(self):
        resp = self.assistente.responder("e se eu tomar banho de 10 minutos?")
        self.assertIn("90,0 kWh", resp.texto)  # 4,5 kW x 10/60 h x 120 banhos
        self.assertIn("a mais", resp.texto)
        self.assertIn("a menos", self.assistente.responder("banho de 5 min").texto)
        self.assertIn("Não consegui", self.assistente.responder("banho de 90 minutos").texto)

    def test_fontes_em_linguagem_simples(self):
        texto = self.assistente.responder("fontes").texto
        self.assertNotIn("_", texto)
        self.assertIn("SunData", texto)
        self.assertIn("ESTIMATIVAS", texto)

    def test_tabela_nao_mostra_retorno_de_opcao_que_nao_se_aplica(self):
        texto = self.assistente.com_situacao(casa_propria=False).responder("comparar").texto
        self.assertEqual(texto.count("não se aplica à sua casa"), 2)

    def test_retorno_maior_que_vida_util_aparece_como_nao_se_paga(self):
        from energia import calculos as calc
        pequeno = calc.PerfilBanho(2, 1, 6, 4400, 2100, 3)
        idosa = self.assistente.com_situacao(perfil=pequeno, consumo_total_kwh_mes=95, tarifa_social=True)
        self.assertIn("não se paga dentro da vida útil", idosa.responder("aquecedor solar").texto)
        recomendacao = idosa.responder("comparar").texto
        self.assertNotIn("confira se tem direito", recomendacao)

    def test_explica_kwh(self):
        self.assertIn("1.000 W", self.assistente.responder("o que é kWh?").texto)

    def test_simulacao_cria_novo_assistente_sem_alterar_o_original(self):
        alugado = self.assistente.com_situacao(casa_propria=False)
        self.assertTrue(self.assistente.entrada.casa_propria)
        self.assertIn("NÃO se aplica", alugado.responder("aquecedor solar").texto)


class TestRelatorio(unittest.TestCase):
    def test_relatorio_usa_os_mesmos_numeros_do_assistente(self):
        from energia.relatorio import gerar_json, gerar_markdown
        assistente = AssistenteEnergia()
        _, alts = assistente.analise()
        md = gerar_markdown(assistente)
        for alt in alts:
            self.assertIn(reais(alt.economia_liquida_ano), md)
        self.assertIn("ESTIMATIVA", md)
        dados = gerar_json(assistente)
        self.assertEqual(len(dados["alternativas"]), 3)
        self.assertAlmostEqual(dados["cenario"]["consumo_chuveiro_kwh_mes"], 72.0)


class TestMain(unittest.TestCase):
    def rodar(self, respostas):
        fila = iter(respostas)
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            main.menu(AssistenteEnergia(), entrada=lambda _: next(fila))
        return saida.getvalue()

    def test_menu_pergunta_e_sai(self):
        saida = self.rodar(["1", "quanto meu chuveiro gasta", "voltar", "0"])
        self.assertIn("kWh por mês", saida)
        self.assertIn("Até logo", saida)

    def test_simulacao_valida_entradas_invalidas(self):
        # moradores: texto, fora da faixa, válido | 4 Enter | conta abaixo do chuveiro, válida | s/n inválido
        respostas = ["2", "abc", "25", "3", "", "", "", "", "10", "120", "talvez", "n", "n", "s", "0"]
        saida = self.rodar(respostas)
        self.assertIn("Digite um número", saida)
        self.assertIn("Valor deve estar entre", saida)
        self.assertIn("Responda s ou n", saida)
        self.assertIn("Recomendação", saida)

    def test_opcao_invalida(self):
        self.assertIn("Opção inválida", self.rodar(["9", "0"]))

    def test_linha_de_comando(self):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            codigo = main.main(["--pergunta", "dicas"])
        self.assertEqual(codigo, 0)
        self.assertIn("VERÃO", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
