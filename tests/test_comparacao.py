import json
import os
import tempfile
import unittest
from dataclasses import replace

from energia import comparacao as cmp
from energia.premissas import carregar_premissas, valores


class TestPremissas(unittest.TestCase):
    def test_toda_premissa_tem_tipo_e_unidade_e_estimados_tem_justificativa(self):
        for p in carregar_premissas().values():
            with self.subTest(chave=p.chave):
                self.assertIn(p.tipo, ("real", "estimado", "hipotese"))
                self.assertTrue(p.unidade)
                if p.tipo == "real":
                    self.assertTrue(p.fonte, "dado real precisa de fonte")
                if p.tipo == "estimado":
                    self.assertTrue(p.fonte or p.observacao, "estimativa precisa de justificativa")

    def test_arquivo_invalido_gera_erro_claro(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump({"x": {"valor": 1, "unidade": "u", "tipo": "chute"}}, f)
        try:
            with self.assertRaises(ValueError):
                carregar_premissas(f.name)
        finally:
            os.remove(f.name)
        with self.assertRaises(FileNotFoundError):
            carregar_premissas("nao_existe.json")


class TestComparacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = valores(carregar_premissas())
        cls.entrada = cmp.entrada_referencia(cls.v)
        cls.cenario, cls.alts = cmp.comparar(cls.entrada, cls.v)

    def test_tres_alternativas_com_pelo_menos_uma_renovavel(self):
        self.assertEqual([a.codigo for a in self.alts], ["A", "B", "C"])
        self.assertTrue(any(a.renovavel for a in self.alts))

    def test_cenario_referencia(self):
        self.assertAlmostEqual(self.cenario.consumo_chuveiro_kwh_mes, 72.0)
        self.assertAlmostEqual(self.cenario.participacao_chuveiro, 0.40)
        self.assertAlmostEqual(self.cenario.tarifa, 0.789 / 0.83)

    def test_habitos_sem_investimento_e_retorno_imediato(self):
        a = self.alts[0]
        self.assertEqual(a.investimento, 0)
        self.assertEqual(a.payback_anos, 0.0)
        # 72 kWh -> 4166,7 W x 5/60 h x 120 banhos = 41,67 kWh/mês
        self.assertAlmostEqual(a.reducao_kwh_ano, (72 - 41.6667) * 12, places=2)

    def test_solar_termico_cobre_fracao_solar(self):
        b = self.alts[1]
        self.assertAlmostEqual(b.cobertura_chuveiro, self.v["solar_termico_fracao_solar"])
        self.assertAlmostEqual(b.saldo_horizonte, b.economia_liquida_ano * 10 - b.investimento)

    def test_fotovoltaica_custo_e_geracao(self):
        c = self.alts[2]
        self.assertAlmostEqual(c.investimento, self.v["fv_custo_kit"] + self.v["fv_custo_instalacao_homologacao"])
        self.assertGreater(c.cobertura_chuveiro, 1.0)  # 1,1 kWp gera mais que o chuveiro usa

    def test_recomendacao_comeca_pelos_habitos_e_ordena_por_retorno(self):
        passos = cmp.recomendar(self.entrada, self.alts)
        self.assertIn("alternativa A", passos[0])
        self.assertTrue(passos[1].startswith("C"))
        self.assertTrue(passos[2].startswith("B"))

    def test_aluguel_torna_solar_inviavel(self):
        alugada = replace(self.entrada, casa_propria=False)
        _, alts = cmp.comparar(alugada, self.v)
        self.assertFalse(alts[1].viavel or alts[2].viavel)
        self.assertIn("assinatura", " ".join(cmp.recomendar(alugada, alts)))

    def test_tarifa_social_reduz_economia_em_reais_quando_consumo_baixo(self):
        baixa = replace(self.entrada, consumo_total_kwh_mes=100, tarifa_social=True)
        _, alts = cmp.comparar(baixa, self.v)
        # só 20 kWh acima da faixa gratuita: economia limitada a 20 kWh/mês
        self.assertLessEqual(alts[0].economia_bruta_ano, 20 * 12 * self.cenario.tarifa + 1e-9)

    def test_fv_nao_reduz_conta_abaixo_do_custo_de_disponibilidade(self):
        pequena = replace(self.entrada, consumo_total_kwh_mes=60)
        _, alts = cmp.comparar(pequena, self.v)
        maximo = (60 - self.v["custo_disponibilidade_kwh"]) * 12 * self.cenario.tarifa
        self.assertAlmostEqual(alts[2].economia_bruta_ano, maximo)

    def test_consumo_total_invalido(self):
        with self.assertRaises(ValueError):
            replace(self.entrada, consumo_total_kwh_mes=0)


if __name__ == "__main__":
    unittest.main()
