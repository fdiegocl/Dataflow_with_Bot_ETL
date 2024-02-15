import os

class Log:    

    # Cria os diretórios de pastas para organizar os arquivos de log.
    def mkDirLog(today):

        if not os.path.isdir('logs'):
            os.mkdir('logs')
        if not os.path.isdir('logs/' + str(today)[0:4]):
            os.mkdir('logs/' + str(today)[0:4])
        if not os.path.isdir('logs/' + str(today)[0:4] + '/' + str(today)[5:7]):
            os.mkdir('logs/' + str(today)[0:4] + '/' + str(today)[5:7])

        day = str(today)[0:4] + str(today)[5:7] + str(today)[8:10]
        log_file = f'logs/{str(today)[0:4]}/{str(today)[5:7]}/{day}.log'

        return log_file