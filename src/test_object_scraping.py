from kv_scraper import  KVBuilder
import util_functions.scraper_utils as scraper_utils

kv_builder = KVBuilder()





def scrape_object(object_id):
  address='https://kv.ee/?act=search.objectinfo&object_id={}'.format(object_id)
  print(address)
  r = kv_builder.session.get(address)
  details=scraper_utils.parse_details_from_html(r)
  return details


def main():
  scrape_ids=[3244096,3096498]
  for i in scrape_ids:
    print(scrape_object(i))

if __name__ == "__main__":
    main()


