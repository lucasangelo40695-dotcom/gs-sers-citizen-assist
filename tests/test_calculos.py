import unittest

from energia import calculos as calc


def perfil(**mudancas):
    base = dict(moradores=4, banhos_por_pessoa_dia=1, duracao_min=8, potencia_inverno_w=5500,
                potencia_verao_w=3500, meses_inverno=6, dias_por_mes=30)
    base.update(mudancas)
    return calc.PerfilBanho(**base)


class TestEnergia(unittest.TestCase):
    def test_energia_e_potencia_vezes_tempo(self):
        self.assertAlmostEqual(calc.energia_kwh(5500, 1), 5.5)
        self.assertAlmostEqual(calc.energia_kwh(1000, 0.5), 0.5)

    def test_potencia_media_ponderada_pelos_meses(self):
        self.assertAlmostEqual(calc.potencia_media_w(perfil()), 4500)
        self.assertAlmostEqual(calc.potencia_media_w(perfil(meses_inverno=12)), 5500)

    def test_consumo_do_chuveiro_cenario_referencia(self):
        # 4,5 kW x (8/60 h) x 4 pessoas x 30 dias = 72 kWh
        self.assertAlmostEqual(calc.consumo_chuveiro_kwh_mes(perfil()), 72.0)

    def test_calor_da_agua_q_igual_m_c_delta_t(self):
        # 100 L de 20 a 40 °C: 100 x 4,186 x 20 / 3600 = 2,3256 kWh
        self.assertAlmostEqual(calc.energia_termica_kwh(100, 20, 40), 2.3256, places=4)

    def test_vazao_confere_com_balanco_de_energia(self):
        vazao = calc.vazao_l_min(4500, 0.95, 20, 38)
        calor = calc.energia_termica_kwh(vazao * 8, 20, 38)
        eletrica = calc.energia_kwh(4500, 8 / 60)
        self.assertAlmostEqual(calor / eletrica, 0.95, places=6)

    def test_tarifa_final_com_reajuste_e_tributos_por_dentro(self):
        self.assertAlmostEqual(calc.tarifa_final(1.0, 0.10, 0.20), 1.375)

    def test_geracao_fotovoltaica(self):
        self.assertAlmostEqual(calc.geracao_fv_kwh_mes(1.0, 4.5, 0.75, 30), 101.25)

    def test_emissao(self):
        self.assertAlmostEqual(calc.emissao_kg(1000, 0.0385), 38.5)


class TestTarifaSocialEPayback(unittest.TestCase):
    def test_sem_isencao_economia_integral(self):
        self.assertAlmostEqual(calc.economia_mensal_reais(180, 150, 1.0), 30)

    def test_com_isencao_so_conta_acima_de_80(self):
        self.assertAlmostEqual(calc.economia_mensal_reais(100, 60, 1.0, isencao_kwh=80), 20)
        self.assertAlmostEqual(calc.economia_mensal_reais(70, 50, 1.0, isencao_kwh=80), 0)

    def test_payback(self):
        self.assertAlmostEqual(calc.payback_anos(1000, 250), 4)
        self.assertEqual(calc.payback_anos(0, 100), 0.0)
        self.assertIsNone(calc.payback_anos(1000, 0))
        self.assertIsNone(calc.payback_anos(1000, -5))


class TestValidacao(unittest.TestCase):
    def test_entradas_invalidas_sao_recusadas(self):
        casos = [dict(moradores=0), dict(duracao_min=0), dict(duracao_min=90),
                 dict(potencia_verao_w=6000), dict(meses_inverno=13), dict(banhos_por_pessoa_dia=0)]
        for caso in casos:
            with self.subTest(caso=caso), self.assertRaises(ValueError):
                perfil(**caso)

    def test_funcoes_recusam_parametros_fisicamente_invalidos(self):
        with self.assertRaises(ValueError):
            calc.energia_termica_kwh(10, 40, 20)
        with self.assertRaises(ValueError):
            calc.vazao_l_min(4500, 1.5, 20, 38)
        with self.assertRaises(ValueError):
            calc.tarifa_final(1, 0, 1)

    def test_perfil_e_imutavel(self):
        with self.assertRaises(Exception):
            perfil().moradores = 2


if __name__ == "__main__":
    unittest.main()
