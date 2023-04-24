import pandas as pd
import sys
import logging
import traceback
import time
import upbit

if __name__ == '__main__':
    try:
        price_data = upbit.current_price('KRW-BTC');
        datalogger = upbit.log()

        # result = upbit.buycoin_mp("KRW-BTC", '10000')
        # datalogger.info(result)
        #
        # result = upbit.sellcoin_mp("KRW-BTC")
        # datalogger.info(result)

        n=0
        while True:
            candles = upbit.get_candle('KRW-BTC', '1', 1)
            price = upbit.current_price('KRW-BTC')
            rsi = upbit.get_rsi('KRW-BTC', '30', '200')
            mfi = upbit.get_mfi('KRW-BTC', '30', '200', 1)
            macd = upbit.get_macd('KRW-BTC', '30', '200', 1)
            signal = macd[0]['SIGNAL']
            bb_data = upbit.get_bb('KRW-BTC', '30', '200', 1)
            bbh = bb_data[0]["BBH"]
            df = pd.DataFrame(candles)
            dfDt = df['candle_date_time_kst'].iloc[::-1]

            Coin_Data = []
            Coin_Data.append(
                {"type": "BTC", "DT": dfDt[0], "PRICE": price, "RSI": rsi, "MFI": round(mfi, 4), "MACD": macd[0]["MACD"],
                 "SIGNAL": macd[0]['SIGNAL'], "OCL": macd[0]['OCL'], "BBH": bb_data[0]["BBH"], "BBM": bb_data[0]["BBM"],
                 "BBL": bb_data[0]["BBL"]})

            print("프로그램 실행중")



            datalogger.info(candles)
            datalogger.info(Coin_Data)


            # 조건이 만족할 때 매수
            if (price > price_data * 1.1):
                result = upbit.buycoin_mp("KRW-BTC", '10000')
                datalogger.info(result)

            #조건이 만족할 때 매도
            if(price < price_data*0.9):
               result = upbit.sellcoin_mp("KRW-BTC")
               datalogger.info(result)






            # if(rsi>55 and mfi<20 and macd>SIGNAL and price<bbh)
            #result = upbit.buycoin_mp("KRW-BTC", '10000')
            # if(rsi<45 and mfi>80 and macd<SIGNAL and price>bbh)
            #result = upbit.sellcoin_mp("KRW-BTC")






    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)