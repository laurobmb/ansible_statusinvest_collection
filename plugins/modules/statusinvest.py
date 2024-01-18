#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: statusinvest
short_description: Module obtains values of Brazilian shares on the website statusinvest.com.br
version_added: "2.8"
description:
  - "Module obtains values of Brazilian shares on the website statusinvest.com.br."
options:
    name:
        description:
          - Name of the person to salute. If no value is provided the default
            value will be used.
        required: false
        type: str
        default: John Doe
author:
    - Lauro Gomes (@laurobmb)
'''

EXAMPLES = r'''
# Pass in a custom name
- name: Get result
  statusinvest:
    statusinvest_acoes: bbas3
    statusinvest_fundos: vghf11
'''

RETURN = r'''
"acoes": {
    "DIVIDEND YIELD": "8,17",
    "NAME": "bbas3",
    "VALOR ATUAL": "55,99"
},
"changed": true,
"failed": false,
"fii": {
    "DIVIDEND YIELD": "13,66",
    "NAME": "vghf11",
    "VALOR ATUAL": "9,52"
}
'''

import random
from ansible.module_utils.basic import AnsibleModule
from lxml import html
import requests, sys

def statusinvest_acoes(ACOES):
    acoes = ACOES
    percentagem_dividendo, cotacao_atual = '0','0'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get('https://statusinvest.com.br/acoes/'+acoes, headers=headers)
        tree = html.fromstring(page.content)
        percentagem_dividendo = "/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong"
        cotacao_atual = '//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong'
        percentagem_dividendo = tree.xpath(percentagem_dividendo)[0].text
        cotacao_atual = tree.xpath(cotacao_atual)[0].text
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        return acoes,percentagem_dividendo, cotacao_atual
    return acoes, percentagem_dividendo, cotacao_atual

def statusinvest_fundos(FUNDO):
    fundo = FUNDO
    valor_do_dividendo, cotacao_atual = '0','0'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get('https://statusinvest.com.br/fundos-imobiliarios/'+fundo, headers=headers)
        tree = html.fromstring(page.content)
        valor_do_dividendo = "/html/body/main/div[2]/div[1]/div[4]/div/div[1]/strong"
        cotacao_atual = '//*[@id="main-2"]/div[2]/div[1]/div[1]/div/div[1]/strong'
        valor_do_dividendo = tree.xpath(valor_do_dividendo)[0].text
        cotacao_atual = tree.xpath(cotacao_atual)[0].text
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        return fundo,valor_do_dividendo, cotacao_atual
    return fundo, valor_do_dividendo, cotacao_atual


def run_module():

    module_args = dict(
            statusinvest_acoes=dict(type='str', default='bbas3'), #required=True),
            statusinvest_fundos=dict(type='str', default='vghf11') #, required=True)
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

    result['acoes']['NAME'] = statusinvest_acoes(module.params['statusinvest_acoes'])[0]
    result['acoes']['DIVIDEND YIELD'] = statusinvest_acoes(module.params['statusinvest_acoes'])[1]
    result['acoes']['VALOR ATUAL'] = statusinvest_acoes(module.params['statusinvest_acoes'])[2]

    result['fii']['NAME'] = statusinvest_fundos(module.params['statusinvest_fundos'])[0]
    result['fii']['DIVIDEND YIELD'] = statusinvest_fundos(module.params['statusinvest_fundos'])[1]
    result['fii']['VALOR ATUAL'] = statusinvest_fundos(module.params['statusinvest_fundos'])[2]

    if module.params['statusinvest_acoes']:
        result['changed'] = True

    if module.params['statusinvest_fundos']:
        result['changed'] = True

    if module.params['statusinvest_acoes'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    if module.params['statusinvest_fundos'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()