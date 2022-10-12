import pandas as pd
from pycoingecko import CoinGeckoAPI
import gspread

sa = gspread.service_account(filename="peaceful-nation-355019-2c3841a74c63.json")
sh = sa.open("coin and price")
wks = sh.worksheet("Sheet1")
cg = CoinGeckoAPI()
source_df = pd.DataFrame(wks.get_all_records())

new_df = source_df.copy()
final_df = source_df.append(new_df)
final_df.to_csv('final.csv', index=False)

for j in range(1, wks.row_count + 1):

    if wks.acell(f"A{j}").value == "None":
        break

    else:
        row_links = wks.acell(f"A{j}").value
        row = row_links.replace("https://www.coingecko.com/en/coins/", "")

        coin_dict = cg.get_price(ids=row, vs_currencies='usd')  # find price

        for value in coin_dict.values():
            usd = value.get('usd')

            wks.update(f'B{j}', usd)
