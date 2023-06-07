#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Author: Elienai Soares

from discord_webhook import DiscordWebhook, DiscordEmbed
import sys

url_webhook = ""
# Pega o primeiro argumento passado para o script
# Caso o argumento for "add", o webhook é enviado posteriormente com a mensagem de adição.
# Qualquer outro argumento resulta em uma mensagem de remoção
condition = sys.argv[1]
# json_data = sys.argv[2]

json_data_teste = {
  "cpus":{
    "46":{
      "MANUFACTURER":"GenuineIntel",
      "TYPE":"Intel(R) Core(TM) i5-3570 CPU @ 3.40GHz",
      "ASSET":"46"
    }
  },
  "memories":{
    "46":{
      "TYPE":"DDR3",
      "CAPACITY (MB)":"4096",
      "ASSET":"46"
    },
    "46*":{
      "TYPE":"DDR3",
      "CAPACITY (MB)":"2048",
      "ASSET":"46"
    }
  },
  "monitors":{
    "46":{
      "MANUFACTURER":"Hewlett Packard",
      "DESCRIPTION":"HWP.3139.01010101 (37\/2014)",
      "ASSET":"46"
    },
    "46*":{
      "MANUFACTURER":"BenQ Corporation",
      "DESCRIPTION":"",
      "ASSET":"46"
    }
  },
  "storages":{
    "46":{
      "MANUFACTURER":"(Standard disk drives)",
      "DISKSIZE (MB)":"476937",
      "MODEL":"\/\/.\/PHYSICALDRIVE0",
      "ASSET":"46"
    }
  },
  "videos":{
    "46":{
      "NAME":"Intel(R) HD Graphics",
      "MEMORY":"2112",
      "ASSET":"46"
    }
  }
}


# Procura pelo nome do ativo modificado que aqui é chamado de "ASSET"
# Caso não encontre, procura recursivamente em todos os valores do dicionário
def get_asset_value(data):
    if "ASSET" in data:
        return data["ASSET"]
    else:
        for value in data.values():
            if isinstance(value, dict):
                result = get_asset_value(value)
                if result is not None:
                    return result
    return "Sem informação do nome do ativo"

# Funcao para processar os dados do json
# Entra em cada dicionario recursivamente extraindo chave e valor ignorando a chave "ASSET"
def process_json_data(data):
    result = []
    for key, value in data.items():
        if isinstance(value, dict):
            if "ASSET" in value:
                result.append(", ".join([f"{k}: '{v}'" for k, v in value.items() if k != 'ASSET']))
            else:
                result.extend(process_json_data(value))
    return result

# Processa os dados do json e retorna uma string com os valores
result_cpus = ", ".join(process_json_data(json_data_teste.get("cpus", {})))
result_memories = ", ".join(process_json_data(json_data_teste.get("memories", {})))
result_monitors = ", ".join(process_json_data(json_data_teste.get("monitors", {})))
result_storages = ", ".join(process_json_data(json_data_teste.get("storages", {})))
result_videos = ", ".join(process_json_data(json_data_teste.get("videos", {})))


# Monta o webhook
bot_name = "OCS - Notification"
title = get_asset_value(json_data_teste)
webhook = DiscordWebhook(url='%s' %(url_webhook))
embed = DiscordEmbed(title='Adição - %s' %(title), color='0x6aff00') if condition == 'add' else DiscordEmbed(title='Remoção - %s' %(title), color='0xCC0000')
embed.set_author(name='%s' %(bot_name))

# Adiciona os campos do webhook
embed.add_embed_field(name='Cpus', value=result_cpus, inline=False)
embed.add_embed_field(name='Memories', value=result_memories, inline=False)
embed.add_embed_field(name='Monitors', value=result_monitors, inline=False)
embed.add_embed_field(name='Storages', value=result_storages, inline=False)
embed.add_embed_field(name='Videos', value=result_videos, inline=False)

# Envia o webhook
webhook.add_embed(embed)
response = webhook.execute(embed)