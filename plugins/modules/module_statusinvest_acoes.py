from lxml import html
import requests, sys


def statusinvest_acoes(ACOES):
    acoes = ACOES
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get('https://statusinvest.com.br/acoes/'+acoes, headers=headers)
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        print(e)
    tree = html.fromstring(page.content)
    percentagem_dividendo = "/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong"
    cotacao_atual = '//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong'
    percentagem_dividendo = tree.xpath(percentagem_dividendo)[0].text
    cotacao_atual = tree.xpath(cotacao_atual)[0].text
    #percentagem_dividendo = percentagem_dividendo.replace(',','.')
    print('Valor do Dividendo da',acoes,percentagem_dividendo)
    print('Valor da cotacao atual da',acoes,cotacao_atual)
    return percentagem_dividendo, cotacao_atual

#if __name__ == '__main__':
#    try:
#        if len(sys.argv) > 0:
#            statusinvest_acoes(sys.argv[1].upper())        
#        else:
#            statusinvest_acoes("IRBR3")
#    except:
#        statusinvest_acoes("IRBR3")
#