from playwright.sync_api import sync_playwright
from datetime import datetime
import modules.log as log
import pandas as pd
import os, shutil, logging, paramiko

# Define a data e hora atual para criar as pastas e arquivos de log
today = datetime.today()
log_file = log.Log.mkDirLog(today)

logging.basicConfig(level=logging.INFO, filename=log_file, format="%(asctime)s - %(levelname)s - %(message)s")

class Bot:   

    logging.info('***INICIALIZANDO PROCESSO***')

    # Cria os diretórios de pastas para organizar os arquivos de entrada e saida.
    def mkDir(today, path):
        logging.info('Funcao mkDir() executada - Organizando pastas...')

        if not os.path.isdir(path):
            os.mkdir(path)
            logging.info(f'Diretorio {path} criado.')

        if not os.path.isdir(path + '/input'):
            os.mkdir(path + '/input')
            logging.info(f'Diretorio {path}/input/ criado.')
        if not os.path.isdir(path + '/input/pending'):
            os.mkdir(path + '/input/pending')
            logging.info(f'Diretorio {path}/input/pending/ criado.')
        if not os.path.isdir(path + '/input/done'):
            os.mkdir(path + '/input/done')
            logging.info(f'Diretorio {path}/input/done/ criado.')
        if not os.path.isdir(path + '/input/done/' + str(today)[0:4]):
            os.mkdir(path + '/input/done/' + str(today)[0:4])
            logging.info(f'Diretorio {path}/input/done/{str(today)[0:4]}/ criado.')
        if not os.path.isdir(path + '/input/done/' + str(today)[0:4] + '/' + str(today)[5:7]):
            os.mkdir(path + '/input/done/' + str(today)[0:4] + '/' + str(today)[5:7])
            logging.info(f'Diretorio {path}/input/done/{str(today)[0:4]}/{str(today)[5:7]}/ criado.')

        if not os.path.isdir(path + '/output'):
            os.mkdir(path + '/output')
            logging.info(f'Diretorio {path}/output/ criado.')
        if not os.path.isdir(path + '/output/pending'):
            os.mkdir(path + '/output/pending')
            logging.info(f'Diretorio {path}/output/pending/ criado.')
        if not os.path.isdir(path + '/output/done'):
            os.mkdir(path + '/output/done')
        if not os.path.isdir(path + '/output/done/' + str(today)[0:4]):
            logging.info(f'Diretorio {path}/output/pending/{str(today)[0:4]}/ criado.')
            os.mkdir(path + '/output/done/' + str(today)[0:4])
        if not os.path.isdir(path + '/output/done/' + str(today)[0:4] + '/' + str(today)[5:7]):
            os.mkdir(path + '/output/done/' + str(today)[0:4] + '/' + str(today)[5:7])
            logging.info(f'Diretorio {path}/output/pending/{str(today)[0:4]}/{str(today)[5:7]}/ criado.')

    # Limpa a pasta, caso existam arquivos residuais de processos anteriores.
    def clearPath(path):
        logging.info('Funcao clearPath() executada - Limpando pastas...')
        logging.info(f'Limpando diretorio {path}.')

        files_types = [".XLS", ".xls", ".CSV", ".csv", ".XML", ".xml", ".XLSX", ".xlsx"]        
        for iten in files_types:
            for file in os.listdir(path):                
                if iten in file:            
                    os.unlink(path + file)
                    logging.info(f'Arquivo {file}, excluido.')

    # Baixa o arquivo com os dados gerados no mes vigente.
    def download_files(today, path, link):
        logging.info('Funcao download_files() executada - Baixando dados...')

        # Navega atraves da pagina do fornecedor
        with sync_playwright() as p:
            logging.info('Navegando na pagina do fornecedor.')            
            # browser     = p.chromium.launch(headless=False)                 # Modo navegador ativo
            browser     = p.chromium.launch()                               # Modo navegador oculto
            page        = browser.new_page()
            page.goto(link)                                                 # Abri a pagina
            logging.info('Pagina inicializada.') 
            page.wait_for_load_state()
            page.locator('xpath=//*[@id="btn_essemes"]').click()            # Clica no botão "Esse Mês"
            logging.info('Click no botao "Esse Mes".') 
            page.wait_for_load_state()
            page.locator('xpath=//*[@id="menu"]/ul/li[3]/a').click()        # Clica no botão "EXPORTAR"
            logging.info('Click no botao "EXPORTAR".')
            page.wait_for_load_state()

            # Clica no botão "Exportar" do quadro "BONUS GERADO" e aguarda o download terminar.
            logging.info('Inicializando Download de Dados.')
            with page.expect_download() as download_info:
                page.locator('xpath=/html/body/div[1]/div[5]/div[3]/div[1]/div/div[3]/button').click()
                logging.info('Click no botao "Esportar" da caixa "BONUS GERADO"')
                page.wait_for_load_state()
            download = download_info.value
            file_name = 'CRMB_Bonus_Gerados_' + str(today)[0:4] + str(today)[5:7] + str(today)[8:10] + "_" + str(today)[11:13] + str(today)[14:16] + ".xlsx"
            download.save_as(path + "/input/pending/" + file_name)

            # Valida se o arquivo foi baixado
            logging.info('Validando Download.')
            file_count = 0
            for file in os.listdir(path + "/input/pending/"):
                if '.XLSX' in file or '.xlsx' in file:
                    file_count = file_count + 1

            if file_count > 0:
                logging.info(f'Download realizado com sucesso. {file_count} arquivo baixado.')
            else:
                logging.info(f'Download não realizado. {file_count} arquivo baixado.')

            return file_count

    # Processa e organiza os dados, da fonte em .xlsx para .csv
    def dataETL(source_path, destiny_path):
        logging.info('Funcao dataETL() executada - Organizando dados...')

        for file in os.listdir(source_path):

            if '.XLSX' in file or '.xlsx' in file:

                if 'CRMB' in file or 'crmb' in file:

                    df = pd.read_excel(source_path + file)

                    df['Venda'] = df['Venda'].str[3:]
                    df['Bônus  Gerado'] = df['Bônus  Gerado'].str[3:]
                    df['Valor do Desconto'] = df['Valor do Desconto'].str[3:]

                    basename = os.path.basename(source_path + file)
                    file_out_name = os.path.splitext(basename)[0] + '.csv'
                    df.to_csv(destiny_path + file_out_name, encoding='utf-8', index=False)

        # Valida se os dados foram processados
        logging.info('Validando processamento de Dados.')
        file_count = 0
        for file in os.listdir(destiny_path):
            if '.CSV' in file or '.csv' in file:
                file_count = file_count + 1

        if file_count > 0:
            logging.info(f'Processamento realizado com sucesso. {file_count} arquivo processado.')
        else:
            logging.info(f'Processamento não realizado. {file_count} arquivo processado.')

        return file_count

    # Organiza os arquivos nas pastas 'files'
    def orgFiles(source_path, destiny_path, move_or_copy):
        logging.info('Funcao orgFiles() executada - Organizando arquivos...')

        files_types = [".XLS", ".xls", ".CSV", ".csv", ".XLSX", ".xlsx"]
        for iten in files_types:
            for file in os.listdir(source_path):
                if iten in file:
                    if move_or_copy == 'move':
                        shutil.move(source_path + file, destiny_path + file)
                        logging.info(f'O arquivo {file} foi movido de {source_path} para {destiny_path}.')
                    elif move_or_copy == 'copy':
                        shutil.copy(source_path + file, destiny_path + file)
                        logging.info(f'O arquivo {file} foi copiado de {source_path} para {destiny_path}.')

                        # Valida se o arquivo foi copiado
                        logging.info('Validando a copia do arquivo.')
                        file_count = 0                        
                        for file in os.listdir(destiny_path):
                            if '.CSV' in file or '.csv' in file:
                                file_count = file_count + 1

                        if file_count > 0:
                            logging.info(f'Copia realizada com sucesso. {file_count} arquivo copiado.')
                        else:
                            logging.info(f'Copia não realizada. {file_count} arquivo copiado.')

                        return file_count

    # Conecta via SSH ao servidor de aplicação e executa a tarefa para carregar os dados no banco.
    def loadData(hostname, port, username, password):
        logging.info('Funcao loadData() executada - Carregando dados...')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname, port, username, password)
            stdin, stdout, stderr = ssh.exec_command('schtasks /run /tn CRMB')
            exit_info = stdout.read().decode()
            ssh.close()

            logging.info(f"Saida do comando SSH: {exit_info}")
            return exit_info
        
        except Exception as e:

            logging.info(f"Erro ao executar comando SSH: {e}")
            return None