from google import google
import psycopg2
from psycopg2 import InternalError
import time

PG_ERROR_TABLE = {
    "VIOLATED_CONSTRAINT" : "25P02"
    # Adicionar códigos de erros aqui, conforme necessário
}

while True:

    try:
        conn = psycopg2.connect("dbname='googledb' user='googlenews' host='localhost' password='googlenews'")
        cur = conn.cursor()
        cur.execute("""SELECT code, words FROM googlenews_search WHERE enabled = true""")
        rows = cur.fetchall()

        for row in rows:

            newsList = google.search_news(row[1])

            for news in newsList:
                content = google.get_content(news.link)

                if content != None:
                     
                    params = {
                        "code": str(row[0]), 
                        "title": news.title, 
                        "url": news.link, 
                        "tmsp": int(news.date)/1000, 
                        "content": content
                    }

                    print()
                    print(news.title)

                    try:
                        cur.execute("""insert into googlenews_content (code, title, url, tmsp, content) values (%(code)s, %(title)s, %(url)s, to_timestamp(%(tmsp)s), %(content)s)""", params)
                     
                    # Pg2 internal error
                    except InternalError as e:

                        # Tabela com códigos de erros do postgres
                        # https://www.postgresql.org/docs/current/static/errcodes-appendix.html#ERRCODES-TABLE
                        # InternalError:
                        #   pgcode
                        #       The error code returned by the backend, if 
                        #       available, else None
                        #   
                        #   pgerror
                        #       The error message returned by the backend, if 
                        #       available, else None

                        if e.pgcode == PG_ERROR_TABLE["VIOLATED_CONSTRAINT"]:
                            print("Title already in database.")
                        # elif e.pgcode == PG_ERROR_TABLE["Other Error"]:
                        else:
                            print("\nUnknown error:" + str(e))

                    # Other errors
                    except Exception as e:
                        print("\nUnknown error:" + str(e))
                    
                    # Commit transaction
                    finally:
                        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()

    except InternalError as e:
        print("Connection failed: " + str(e))
    
    except Exception as e:
        print("Unknown error: " + str(e))

    # Wait 15minutes to update db
    time.sleep(15*60)


