<h2> Projeto de Busca de Locais </h2>

<p> Este repositório contém dois projetos independentes de busca de locais utilizando a API do Google Places. Ambos projetos buscam locais a partir de um termo de pesquisa e localização informados pelo usuário, porém as funcionalidades e implementações são diferentes. </p>

<h3> Projeto 1 - code.py </h3>

<p> Este projeto solicita ao usuário um nicho de interesse e uma localização, em seguida busca locais utilizando a API do Google Places. Para cada local encontrado, são buscados o telefone e o e-mail, quando disponíveis. As informações coletadas são armazenadas em um Pandas DataFrame e exportadas para um arquivo CSV. </p>

<p> Requisitos </p>
<ul>
<li> Python 3 </li>
<li> requests </li>
<li> pandas </li>
</ul>

<p> Como usar </p>
<ol>
<li> Clone este repositório em sua máquina. </li>
<li> Execute o arquivo code.py em um ambiente Python 3. </li>
<li> Siga as instruções apresentadas no terminal para informar o nicho de interesse e a localização desejada. </li>
<li> O resultado será salvo em um arquivo CSV chamado resultado.csv na pasta do projeto. </li>
</ol>

<h3> Projeto 2 - versao2.py </h3>

<p> Este projeto também solicita ao usuário um termo de pesquisa e uma localização, porém busca locais que possuem um determinado curso na área da saúde em seu site. Pode ser modificado para encontrar cursos em outras áreas de graduação. O usuário pode informar quantos resultados deseja obter. As informações coletadas são armazenadas em um Pandas DataFrame e exportadas para um arquivo CSV. </p>

<p> Requisitos </p>
<ul>
<li> Python 3 </li>
<li> requests </li>
<li> pandas </li>
<li> urllib3 </li>
<li> tenacity </li>
</ul>

<p> Como usar </p>
<ol>
<li> Clone este repositório em sua máquina. </li>
<li> Execute o arquivo versao2.py em um ambiente Python 3. </li>
<li> Edite as variáveis termo_busca, localizacao, cursos_saude (informando o curso que deseja buscar), num_resultados e chave_api com as informações desejadas. </li>
<li> O resultado será salvo em um arquivo CSV chamado resultados.csv na pasta do projeto. </li>
</ol>

<p> Licença </p>
<p> Este projeto está licenciado sob a licença GPL-3.0. Consulte o arquivo LICENSE para obter mais informações. </p>
