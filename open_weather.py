!pip install requests

import requests
import time
import sqlite3


def sql_connector():
  con = sqlite3.connect("openweather.db")
  cur = con.cursor()
  return con, cur


def create_table(con, cur, city):
  table_name = city.replace(" ", "_").lower()
  cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (datetime TEXT, temp REAL, humidity INTEGER)")
  con.commit()


def insert_data(con, cur, city, data):
  table_name = city.replace(" ", "_").lower()
  values = (time.ctime(time.time()), data["main"]["temp"], data["main"]["humidity"])
  cur.execute(f"INSERT INTO {table_name} VALUES(?, ?, ?)", values)
  con.commit()


def get_weather_data(city, api_key="077b77612bf4a156d84abb14458b2c8a"):
  url_weather = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
  r = requests.get(url=url_weather)
  return r.json()


def main():
  cities = ["Tehran", "Isfahan", "Paris"]
  api_key = "077b77612bf4a156d84abb14458b2c8a"

  con, cur = sql_connector()

  for city in cities:
    create_table(con, cur, city)

  try:
    while True:
      for city in cities:
        data_weather = get_weather_data(city, api_key)
        insert_data(con, cur, city, data_weather)
        print(f"Data for {city}: {data_weather}")
      time.sleep(20)
  except KeyboardInterrupt:
    pass
  finally:
    con.close()


if __name__ == "__main__":
  main()
