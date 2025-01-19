import random


class TestUtil:

    countyCodes = ["US", "AU", "CA", "CN", "DE", "FR",
                   "GB", "HK", "IN", "JP", "KR", "NL", "SG", "TW"]
    ricCodes = ["AAPL.O", "MSFT.O", "GOOGL.O", "AMZN.O", "FB.O", "TSLA.O", "BRKb.O", "JPM.N", "JNJ.N", "V.N", "WMT.N", "PG.N", "MA.N", "UNH.N", "INTC.O", "VZ.N", "HD.N", "DIS.N", "KO.N", "MRK.N", "PFE.N", "PEP.O", "CSCO.O", "CMCSA.O", "NFLX.O", "T.N", "NVDA.O", "ADBE.O", "XOM.N", "BAC.N", "ABT.N", "CVX.N", "WFC.N", "C.N", "ORCL.N", "BA.N", "ABBV.N", "TMO.N", "ACN.N", "AMGN.O", "MCD.N", "IBM.N", "HON.N", "NKE.N", "TXN.O", "MDT.N", "QCOM.O", "LLY.N", "DHR.N", "PYPL.O", "PM.N", "NEE.N", "UNP.N", "LIN.N", "SBUX.O", "AMT.N", "UPS.N",
                "LOW.N", "CAT.N", "COST.O", "GS.N", "MS.N", "CHTR.O", "BLK.N", "TGT.N", "NOW.N", "AMD.O", "INTU.O", "MMM.N", "ADP.O", "ISRG.O", "CVS.N", "LMT.N", "AXP.N", "MO.N", "SPGI.N", "CME.O", "BK.N", "TJX.N", "ZTS.N", "ANTM.N", "COP.N", "CSX.O", "PLD.N", "CCI.N", "BDX.N", "CL.N", "FIS.N", "SYK.N", "GILD.O", "FISV.O", "SO.N", "DUK.N", "TFC.N", "BMY.N", "ADI.O", "ADSK.O", "KMB.N", "AON.N", "VRTX.O", "REGN.O", "ILMN.O", "SRE.N", "NOC.N", "ITW.N", "EMR.N", "GD.N", "ETN.N", "PNC.N", "SHW.N", "APD.N", "ECL.N", "WM.N", "NSC.N", "ROP.N", "AEP.N"]
    alredyGeneratedCodes = []

    @staticmethod
    def _genRandomInt() -> str:
        return str(random.randint(0, 999999999999)).zfill(12)

    @staticmethod
    def _genISIN() -> str:
        return TestUtil.countyCodes[random.randint(
            0, len(TestUtil.countyCodes)-1)] + TestUtil._genRandomInt()

    @staticmethod
    def _genSEDOL() -> str:
        return TestUtil._genRandomInt()[:7]

    @staticmethod
    def _genRIC() -> str:
        return TestUtil.ricCodes[random.randint(
            0, len(TestUtil.ricCodes)-1)]

    @staticmethod
    def genISIN() -> str:
        code = TestUtil._genISIN()
        cycle = 0
        while code in TestUtil.alredyGeneratedCodes and cycle < 100:
            code = TestUtil._genISIN()
            cycle += 1
        if cycle >= 100:
            raise RuntimeError("Failed to generate unique ISIN code")

        TestUtil.alredyGeneratedCodes.append(code)
        return code

    @staticmethod
    def genSEDOL() -> str:
        code = TestUtil._genSEDOL()
        cycle = 0
        while code in TestUtil.alredyGeneratedCodes and cycle < 100:
            code = TestUtil._genSEDOL()
            cycle += 1
        if cycle >= 100:
            raise RuntimeError("Failed to generate unique SEDOL code")
        TestUtil.alredyGeneratedCodes.append(code)
        return code

    @staticmethod
    def genRIC() -> str:
        code = TestUtil._genRIC()
        cycle = 0
        while code in TestUtil.alredyGeneratedCodes and cycle < 100:
            code = TestUtil._genRIC()
            cycle += 1
        if cycle >= 100:
            raise RuntimeError("Failed to generate unique RIC code")
        TestUtil.alredyGeneratedCodes.append(code)
        return code
