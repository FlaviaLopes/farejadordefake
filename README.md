farejadordefake
==============================

***
# Hackathon Visagio - 2020.2 🏆🏃
***
![farejador-de-fakes](https://github.com/FlaviaLopes/farejadordefake/blob/master/docs/imagens/logo.png)

> Desafio - "Em sua terceira edição, o Hackathon Data Science Visagio buscará entender como os dados podem ajudar no combate às fake news na área da saúde."

❗Abaixo estão informações e instruções para executar a aplicação localmente.
***

***
## Equipe
***

> #### Flávia Lopes (desenvolvedora) 
> ![lopes-flavia](https://github.com/FlaviaLopes/farejadordefake/blob/master/docs/imagens/equipe/flavia.jpeg)
>
> Graduanda em Análise e Desenvolvimento de Sistemas pelo Instituto Federal de Educação, Ciência e Tecnologia de Goiás. Interessada em Ciência de Dados, Código limpo, Inteligência Artificial. Procurando aprender e se aperfeiçoar em Big Data e IA. Já programou em PHP, Java, C e Python. C é demais! Mas fico com o Python. Gosto de desafios! Hackatons são boas maneiras de conhecer novas tecnologias e acompanhar o mercado.
>
> <a href="https://www.linkedin.com/in/lopesflavia">
> <img style="width: 100px; max-width: 200px;" src="https://img.shields.io/badge/lopes-flavia-2684b1?style=for-the-badge?&amp;logo=linkedin">
> </a> <a href="https://www.github.com/FlaviaLopes"> <img style="width: 100px; max-width: 200px;" src="https://img.shields.io/badge/lopes-flavia-000000?style=for-the-badge?&amp;logo=github">
> </a> 

> #### Gabriel (desenvolvedor) 
> ![gabriel](https://github.com/FlaviaLopes/farejadordefake/blob/master/docs/imagens/equipe/gabriel.jpeg)
>
> Aluno da Universidade Federal do ABC, matriculado no curso matutino de Engenharia de Automação, Instrumentação e Robótica. Durante 4 anos, ministrei aulas particulares para alunos de nível médio. Hoje em dia estou atuando com automação na área de Informes Legais situada na diretoria de Wealth Management and Services(WMS) do Itaú Unibanco. Felicidade para mim é, em parte, sentir que existe propósito em meu trabalho. 
> 
> <a href="https://www.linkedin.com/in/gabriel-munaro-2934a937/">
> <img style="width: 100px; max-width: 200px;" src="https://img.shields.io/badge/gabriel-munaro-2684b1?style=for-the-badge?&amp;logo=linkedin">
> </a>

> #### José Cleiton (desenvolvedor) 
> ![josé-cleiton](https://github.com/FlaviaLopes/farejadordefake/blob/master/docs/imagens/equipe/cleiton.jpeg)
>
> Uma pessoa se encontrando no mundo e criando seu próprio caminho, que entende que por mais que a sociedade nos apresente uma série de caminhos a qual ela acha que devemos seguir, o amanhã é na verdade como uma tela em branco e nós podemos pintar a realidade que almejamos.
Curso Sistemas de Informação na UFBA. Apaixonado por: Desenvolvimento Web e Mobile, Filosofia, Psicologia, Empreendedorismo.
>
> <a href="https://www.linkedin.com/in/jos%C3%A9-cleiton-149524182/">
> <img style="width: 100px; max-width: 200px;" src="https://img.shields.io/badge/jose-cleiton-2684b1?style=for-the-badge?&amp;logo=linkedin">
> </a>

> #### Luana Isa Drumond (marketing) 
> ![luana-drumond](https://github.com/FlaviaLopes/farejadordefake/blob/master/docs/imagens/equipe/luana.jpeg)
>
> Sou uma profissional com vivência em Supply Chain, controle de estoques e desenvolvimento de novos fornecedores. Atuei na pesquisa de mercado, análise da concorrência e elaboração de estratégias. Tenho conhecimento em diagrama de Ishikawa; fluxograma (Visio); gráfico de Gantt; Pert CPM; SWOT; Value Stream Map; Matriz GUT; Design Thinking; Lean; Melhoria de Processos; 6 sigma e Projetos. Possuo cursos Green Belt (EDTI); Excel Recursos Avançados (SENAC); MS Project (SENAC) e MBAJr (IEG). Tenho experiência internacional com inglês fluente e espanhol intermediário.
>
> <a href="https://www.linkedin.com/in/luanaisa/">
> <img style="width: 100px; max-width: 200px;" src="https://img.shields.io/badge/luanaisa-2684b1?style=for-the-badge?&amp;logo=linkedin">
> </a>

***
## Organização do Projeto
***
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
