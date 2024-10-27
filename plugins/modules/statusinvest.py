#!/usr/bin/python

import random
from ansible.module_utils.basic import AnsibleModule
from lxml import html
import requests, sys

DOCUMENTATION = '''
---
module: statusinvest
short_description: Module obtains values of Brazilian shares on the website statusinvest.com.br
version_added: "2.8"
description:
  - "Module obtains values of Brazilian shares on the website statusinvest.com.br."
options:
    statusinvest_acoes:
        description:
          - Código da ação (ticker) para obter as informações.
        required: false
        type: str
        default: bbas3
    statusinvest_fundos:
        description:
          - Código do fundo imobiliário (ticker) para obter as informações.
        required: false
        type: str
        default: vghf11
author:
    - Lauro Gomes (@laurobmb)
'''

EXAMPLES = '''
- name: Get result
  statusinvest:
    statusinvest_acoes: bbas3
    statusinvest_fundos: vghf11
'''

RETURN = '''
acoes:
    description: Dados da ação solicitada
    type: dict
    returned: always
    sample: { "NAME": "bbas3", "DIVIDEND YIELD": "8,17", "VALOR ATUAL": "55,99" }
fii:
    description: Dados do fundo imobiliário solicitado
    type: dict
    returned: always
    sample: { "NAME": "vghf11", "DIVIDEND YIELD": "13,66", "VALOR ATUAL": "9,52" }
changed:
    description: Indica se houve uma alteração
    type: bool
    returned: always
'''

def statusinvest_acoes(ACOES):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(f'https://statusinvest.com.br/acoes/{ACOES}', headers=headers)
        tree = html.fromstring(page.content)
        percentagem_dividendo = tree.xpath("/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong")[0].text
        cotacao_atual = tree.xpath('//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong')[0].text
        return ACOES, percentagem_dividendo, cotacao_atual
    except Exception:
        return ACOES, '0', '0'

def statusinvest_fundos(FUNDO):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(f'https://statusinvest.com.br/fundos-imobiliarios/{FUNDO}', headers=headers)
        tree = html.fromstring(page.content)
        valor_do_dividendo = tree.xpath("/html/body/main/div[2]/div[1]/div[4]/div/div[1]/strong")[0].text
        cotacao_atual = tree.xpath('//*[@id="main-2"]/div[2]/div[1]/div[1]/div/div[1]/strong')[0].text
        return FUNDO, valor_do_dividendo, cotacao_atual
    except Exception:
        return FUNDO, '0', '0'

def run_module():
    module_args = dict(
        statusinvest_acoes=dict(type='str', default='bbas3'),
        statusinvest_fundos=dict(type='str', default='vghf11')
    )

    result = dict(
        changed=False,
        acoes={},
        fii={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    # Obtendo dados de ações e fundos
    acoes = statusinvest_acoes(module.params['statusinvest_acoes'])
    fundos = statusinvest_fundos(module.params['statusinvest_fundos'])

    # Populando resultado com dados de ações e fundos
    result['acoes'] = {
        'NAME': acoes[0],
        'DIVIDEND YIELD': acoes[1],
        'VALOR ATUAL': acoes[2]
    }
    result['fii'] = {
        'NAME': fundos[0],
        'DIVIDEND YIELD': fundos[1],
        'VALOR ATUAL': fundos[2]
    }

    # Marcando como alterado se foram passados parâmetros para ações ou fundos
    if module.params['statusinvest_acoes'] or module.params['statusinvest_fundos']:
        result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

if __name__ == '__main__':
    main()
