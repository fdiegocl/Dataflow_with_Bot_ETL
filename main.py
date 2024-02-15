from datetime import datetime
import modules.bot as bot
import json

if __name__ == '__main__':

    # Instancia a classes Bot e Logs
    bot = bot.Bot

    # Define a data e hora atual
    today = datetime.today()

    # Acessa em modo de leitura o arquivo config.json
    config_file = "config/config.json"
    with open(config_file, 'r') as file:
        config = json.load(file)

    # Definição de variáveis
    link                = config['link']
    path                = config['files_path']
    input_pending       = path + '/input/pending/'
    output_pending      = path + '/output/pending/'
    moment_path         = str(today)[0:4] + '/' + str(today)[5:7] + '/'
    input_done          = path + '/input/done/' + moment_path
    output_done         = path + '/output/done/' + moment_path
    application_path    = config['application_path']
    hostname            = config['host']['hostname']
    port                = config['host']['port']
    username            = config['host']['username']
    password            = config['host']['password']

    # Organiza as pastas
    bot.mkDir(today, path)

    # Limpa as pastas
    bot.clearPath(input_pending)
    bot.clearPath(output_pending)

    # Baixa os dados
    return_01 = bot.download_files(today, path, link)

    if return_01 > 0:
        # Organiza os dados
        return_02 = bot.dataETL(input_pending , output_pending)

        if return_02 > 0:
            # Organiza os arquivos
            return_03 = bot.orgFiles(output_pending, application_path, 'copy')
            bot.orgFiles(output_pending, output_done, 'move')
            bot.orgFiles(input_pending, input_done, 'move')

            if return_03 > 0:
                # Carrega os dados
                bot.loadData(hostname, port, username, password)