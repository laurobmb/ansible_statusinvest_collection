from lxml import html
import requests, sys


def statusinvest_fundos(FUNDO):
    fundo = FUNDO
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get('https://statusinvest.com.br/fundos-imobiliarios/'+fundo, headers=headers)
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        print(e)
    tree = html.fromstring(page.content)
    valor_do_dividendo = "/html/body/main/div[2]/div[1]/div[4]/div/div[1]/strong"
    ultimo_recebimento = "/html/body/main/div[2]/div[7]/div[2]/div/div[1]/strong"
    cotatacao_atual = '//*[@id="main-2"]/div[2]/div[1]/div[1]/div/div[1]/strong'
    valor_do_dividendo = tree.xpath(valor_do_dividendo)[0].text
    ultimo_recebimento = tree.xpath(ultimo_recebimento)[0].text
    cotatacao_atual = tree.xpath(cotatacao_atual)[0].text
    #valor_do_dividendo = valor_do_dividendo.replace(',','.')
    #ultimo_recebimento = ultimo_recebimento.replace(',','.')
    print(
        'Fundo analisado:', fundo,"\n"+
        'Valor do Dividendo:', valor_do_dividendo,"\n"+
        'Ultimo Recebimento:',ultimo_recebimento,"\n"+
        'Cotação Atual:',cotatacao_atual)
    return valor_do_dividendo, ultimo_recebimento, cotatacao_atual

#
#if __name__ == '__main__':
#    try:
#        if len(sys.argv) > 0:
#            statusinvest_fundos(sys.argv[1].upper())        
#        else:
#            statusinvest_fundos("VGHF11")
#    except:
#        statusinvest_fundos("VGHF11")
