-------------------------------------------------------------------------------------------------------

    Developer   : Diego Carvalho
    Linkedin    : https://www.linkedin.com/in/fdiegocl/

-------------------------------------------------------------------------------------------------------

    Esse projeto tem como objetivo.

-   Automatizar o processo de baixar, tratar e carregar dados de um determinado fornecedor,
    para um banco de dados local, que disponibiliza dados para uma aplicação BI.

    O fluxo do projeto é feito na seguinte sequência.

-   Prepara e organizar as pastas de destino de acordo com ano e mês, para arquivos de dados e logs.
-   Navega, filtra e baixa a partir da página web do fornecedor os dados na forma bruta.
-   Processa, organiza e salva os dados.
-   Copia o arquivo com os dados prontos para um diretório determinado especificado pela aplicação.
-   Acessa via SSH o servidor da aplicação, inicializa uma tarefa, que inicia um script PHP,
    responsável por consumir os dados do arquivo, aplicar as regras de negócio e alimentar o banco
    de dados da aplicação BI.
-   Todo o fluxo descrito acima, alimento arquivos de logs, organizados em pastas por ano e mês,
    para fácil análise posterior em caso de erros no processo.

-------------------------------------------------------------------------------------------------------

    This project aims to:

-   Automate the process of downloading, processing and uploading data from a given supplier,
    to a local database, which makes data available to a BI application.

    The project flow is done in the following sequence.

-   Prepare and organize destination folders according to year and month, for data files and logs.
-   Browse, filter and download raw data from the supplier's website.
-   Processes, organizes and saves data.
-   Copies the file with the ready data to a specific directory specified by the application.
-   Accesses the application server via SSH, initializes a task, which starts a PHP script,
    responsible for consuming file data, applying business rules and feeding the bank
    BI application data.
-   The entire flow described above feeds log files, organized into folders by year and month,
    for easy later analysis in case of errors in the process.

-------------------------------------------------------------------------------------------------------