import os
import yaml


def read_in(base_path='./configs/'):
  res_dict = {}
  for filename in os.listdir(base_path):
    with open(os.path.join(base_path, filename), 'r') as file:
      inf = yaml.load(file, Loader=yaml.FullLoader)
      res_dict.update(inf)
  return res_dict


def get_yaml(source, param, service=None, base_path='./configs/'):
  if service is None:
    key = f'/{source}/'
  else:
    key = f'/{source}/{service}/'

  res_dict = read_in(base_path=base_path)

  return (res_dict[key][param])


def check_key_in_yaml(source,param, service=None , base_path='./configs/'):
  if service is None:
    key = f'/{source}/'
  else:
    key = f'/{source}/{service}/'
  res_dict = read_in(base_path=base_path)
  return param in res_dict[key]
