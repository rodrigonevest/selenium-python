from requests.api import head, options, request
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import pandas as pd

class ChromeAuto:
    def __init__(self): 
        #configuração do browser               
        self.driver_path = 'chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                           'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                            'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36'
        ]        
        #desativando extensão, maximizando a pagina, passando cabeçalhos, etc        
        UA = random.choice(self.user_agent)        
        self.options.add_argument(f'user-agent={UA}') 
        self.options.add_argument('desable-blink-features=AutomationControlled')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--incognito")
        self.options.add_argument("--disable-plugins-discovery")
        self.options.add_argument("--start-maximized")              
        
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options            
        )
        self.chrome.delete_all_cookies()
              
    #função para clicar em departamentos, após em eletrodoméstico e por fim em refrigeradores
    def clica_eletrodomestico(self):
        self.df_refrigerador = pd.DataFrame(index=['URL','DESCRIÇÃO','CÓDIGO'])        
        try:  
            #clicando em departamentos          
            self.btn_departamento = self.chrome.find_element_by_xpath('//*[@id="aspnetForm"]/header/div[1]/div[3]/div/nav')            
            self.btn_departamento.click()

            #função para passa o mouse em cima do botão eletrodoméstico
            self.btn_eletrodomestico = self.chrome.find_element_by_xpath('//*[@id="aspnetForm"]/header/div[1]/div[3]/div/nav/ul/li/ul/li[5]/a')         
            self.Hover = ActionChains(self.chrome).move_to_element(self.btn_eletrodomestico)
            self.Hover.perform()

            #clicando na opção refrigerador    
            self.btn_refigerador = self.chrome.find_element_by_xpath('//*[@id="submenu-eletrodomesticos"]/ul/li[1]/ul/li[2]/a')                        
            self.btn_refigerador.click()

        except Exception as e:
            print('Erro ao clicar em Eletrodoméstico', e)            
        #usando BeautifulSoup para pegar os dados 
        soup = self.chrome.get(self.btn_refigerador)
        index = BeautifulSoup(soup, 'html.parser')
        links = index.find('div',{'class':'Item-sc-10xgy2z-0 gZYlRk'}) 
        links = links.find_all('a',href=True)

        #percorrendo os links de refrigeradores
        for link in links:
            refri = BeautifulSoup(link.data, 'html.parser')
            descriicao = refri.find('div',{'class':'css-1jjcxt1 e1c9wg811'})
            cod = refri.find('div',{'class':'css-1jjcxt1 e1c9wg811'})
                
            #extraindo a descrição e o codigo do item, fazendo alguma limpezas no texto
            if descriicao != None:
                descriicao = [y.get_text(strip=True) for y in refri.find_all('h1')]      
                descriicao = str(descriicao)
                descriicao = descriicao.replace("['",'')
                descriicao = descriicao.replace("']",'')
                descriicao = descriicao.replace('["','')
                descriicao = descriicao.replace('"]','')
                descriicao = descriicao.replace("', '",'')

                cod = [y.get_text(strip=True) for y in refri.find_all('p')]      
                cod = str(cod)
                cod = cod.replace("['",'')
                cod = cod.replace("']",'')
                cod = cod.replace('["','')
                cod = cod.replace('"]','')
                cod = cod.replace("', '",'')

                df_refrigerador = df_refrigerador.append({'URL': link,
                                                                'DESCRIÇÃO': descriicao,
                                                                'CÓDIGO': cod},
                                                                ignore_index=True)
        return self.df_refrigerador               
            


    #função para clicar em departamentos, após em informática e por fim em impressoras
    def clica_informatica(self):
        self.df_impressora = pd.DataFrame(index=['URL','DESCRIÇÃO','CÓDIGO'])         
        try: 
            #clicando em departamentos           
            self.btn_departamento = self.chrome.find_element_by_xpath('//*[@id="aspnetForm"]/header/div[1]/div[3]/div/nav')            
            self.btn_departamento.click()

             #função para passa o mouse em cima do botão informática
            self.btn_informatica = self.chrome.find_element_by_xpath('//*[@id="aspnetForm"]/header/div[1]/div[3]/div/nav/ul/li/ul/li[4]/a')            
            Hover = ActionChains(self.chrome).move_to_element(self.btn_informatica)
            Hover.perform()

            #clicando na opção impresora 
            self.btn_impresora = self.chrome.find_element_by_xpath('//*[@id="submenu-informatica"]/ul/li[4]/ul/li[3]/a')                      
            self.btn_impresora.click()

           
        except Exception as e:
            print('Erro ao clicar em Informática', e)

                #usando BeautifulSoup para pegar os dados 
        soup = self.chrome.get(self.btn_refigerador)
        index = BeautifulSoup(soup, 'html.parser')
        links = index.find('div',{'class':'Row-sc-1s8ruxj-0 iWSNLk'}) 
        links = links.find_all('a',href=True)

        #percorrendo os links de impressoras
        for link in links:
            impre = BeautifulSoup(link.data, 'html.parser')
            descriicao = impre.find('div',{'class':'css-1jjcxt1 e1c9wg811'})
            cod = impre.find('div',{'class':'css-1jjcxt1 e1c9wg811'})
                
            #extraindo a descrição e o codigo do item
            if descriicao != None:
                descriicao = [y.get_text(strip=True) for y in impre.find_all('h1')]      
                descriicao = str(descriicao)
                descriicao = descriicao.replace("['",'')
                descriicao = descriicao.replace("']",'')
                descriicao = descriicao.replace('["','')
                descriicao = descriicao.replace('"]','')
                descriicao = descriicao.replace("', '",'')

                cod = [y.get_text(strip=True) for y in impre.find_all('p')]      
                cod = str(cod)
                cod = cod.replace("['",'')
                cod = cod.replace("']",'')
                cod = cod.replace('["','')
                cod = cod.replace('"]','')
                cod = cod.replace("', '",'')

                df_impressora = df_impressora.append({'URL': link,
                                                                'DESCRIÇÃO': descriicao,
                                                                'CÓDIGO': cod},
                                                                ignore_index=True)
        return self.df_impressora
    # Falta fazer a opção dos televisores
    ############################
    ##########################
    #unindo os dataframes
    def dataframe(self):
        df = [self.df_impressora,self.df_refrigerador]

        result = pd.concat(df)
        result.dropna(inplace=True)
        result.head(-1) 

    #função para acessar o site
    def acessa(self, site):
        teste = self.chrome.get(site)
        #print(self.chrome.title)

     #função para volta a página     
    def voltar(self):
        self.chrome.back() 

     #função para fechar o browser       
    def sair(self):
        self.chrome.quit()

base = 'https://www.extra.com.br'

#realizando as ações
if __name__ == '__main__':
    chrome = ChromeAuto()
    chrome.acessa(base)    
    sleep(5)
    chrome.clica_eletrodomestico()
    sleep(5)
    chrome.voltar() 
    chrome.clica_informatica()    
    sleep(5)    
    chrome.voltar()

    chrome.sair()
    chrome.dataframe()