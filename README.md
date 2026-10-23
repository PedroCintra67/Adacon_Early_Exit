# AdaCon + Early Exit

**Detecção de objetos com processamento adaptativo e saídas antecipadas.**

Projeto de pesquisa desenvolvido na **UFRJ**, no contexto do **Grupo de Teleinformática e Automação (GTA)**, e apresentado no **SIAC 2026** como *Integração de saídas antecipadas em ramos especializados por contexto para detecção de objetos*.

**Autores da apresentação:** Pedro Cintra Silveira, Miguel Elias M. Campista e Daniel Sadoc Menasche.

O objetivo foi investigar se uma rede de detecção consegue reduzir o processamento de imagens menos complexas por meio de saídas intermediárias, preservando a maior parte da qualidade de detecção.

## Arquitetura

O trabalho parte do **AdaCon**, uma arquitetura adaptativa baseada em YOLO. O processamento é organizado em quatro componentes:

1. **Backbone compartilhado:** extrai características da imagem, como bordas, formas e texturas.
2. **Branch Controller:** decide quais ramos especializados devem ser utilizados para a cena.
3. **Ramos especializados:** processam conjuntos de classes agrupadas conforme sua coocorrência em imagens.
4. **Cabeças de detecção:** transformam as características em predições de classes e caixas delimitadoras.

A proposta avaliada incorpora **saídas antecipadas (*early exits*)** em pontos intermediários. A confiança da predição é comparada a um limiar `τ`: se atinge o valor exigido, a imagem pode encerrar o processamento; caso contrário, segue até a saída final. Foram avaliados diferentes critérios para agregar a confiança, como média, média ponderada, mediana e mínimo.

### Configurações comparadas

| Configuração | Ramos | Classes por ramo | Contextos |
|:--|--:|:--|:--|
| **2B** | 2 | 49 e 47 | Ambiente externo / ambiente interno |
| **3B** | 3 | 40, 25 e 47 | Animais e esporte / rua / ambiente interno |
| **4B** | 4 | 40, 25, 23 e 40 | Animais e esporte / rua / sala / cozinha |

Os grupos podem compartilhar classes, por isso suas quantidades não somam necessariamente 80. O recorte do código AdaCon original disponível em `baseline/adacon/` inclui a configuração de **quatro ramos**.

## Dataset: COCO 2017

O estudo usou o **Microsoft COCO 2017**, dataset de detecção de objetos com **80 classes** e imagens reais contendo pessoas, animais, veículos, objetos cotidianos, oclusões e diferentes escalas.

A divisão registrada **no slide 5 da apresentação do SIAC** é:

| Conjunto | Imagens | Utilização |
|:--|--:|:--|
| **Treinamento** | **113.287** | Treinamento da rede |
| **Calibração** | **5.000** | Escolha de camadas, métodos e limiares |
| **Validação** | **5.000** | Comparação final das configurações |
| **Resolução de entrada** | **416 × 416 pixels** | Dimensão utilizada nos experimentos |

O conjunto oficial `train2017` contém 118.287 imagens; a divisão informada no SIAC reserva 5.000 para calibração e mantém 113.287 no treino. As outras 5.000 são do `val2017` oficial. A lista de imagens selecionadas para calibração não está incluída no material deste repositório.

Dataset e anotações: [COCO](https://cocodataset.org/#download).

## Metodologia

O procedimento apresentado no SIAC foi:

1. Treinar o AdaCon e comparar as arquiteturas de **2, 3 e 4 ramos**.
2. Treinar saídas intermediárias e avaliar as camadas **49, 52, 55, 58 e 61**.
3. Comparar métodos de decisão, incluindo média, média ponderada, mínimo e mediana.
4. Avaliar limiares de confiança `τ` entre **0,00 e 1,00**, em passos de **0,05**.
5. Escolher as melhores configurações e medir qualidade, custo e frequência de saída antecipada.

As métricas utilizadas foram **COCO AP (AP50:95)**, precisão média com limiares IoU de 0,50 a 0,95; **GMAC por imagem**, bilhões de operações de multiplicação e acumulação no caminho executado; **% EE**, porcentagem de imagens que saíram antecipadamente; e **AP preservado**, razão entre o AP com saída e o AP da respectiva base.

## Resultados do SIAC 2026

### AdaCon sem saída antecipada — slide 11

| Modelo | COCO AP | GMAC | AP/GMAC |
|:--|--:|--:|--:|
| **2B** | **0,2546** | 28,039 | **0,009081** |
| 3B | 0,2331 | 27,169 | 0,008578 |
| 4B | 0,2268 | **26,735** | 0,008485 |

A configuração **2B** teve a maior qualidade de detecção e foi selecionada como referência.

### Escolha da camada — slide 12

| Camada | COCO AP | GMAC da rota | AP/GMAC |
|--:|--:|--:|--:|
| 49 | 0,0968 | **16,879** | 0,0057 |
| 52 | 0,1061 | 17,765 | 0,0060 |
| 55 | 0,1184 | 18,651 | 0,0063 |
| 58 | 0,1333 | 19,537 | 0,0068 |
| **61** | **0,1504** | 20,423 | **0,0074** |

A **camada 61** apresentou o maior AP e a melhor relação AP/GMAC entre as posições estudadas.

### Métodos de decisão — slide 13 (calibração)

| Método | `τ` | COCO AP | GMAC | % EE |
|:--|--:|--:|--:|--:|
| Média | 0,40 | 0,2565 | 27,447 | 11,50% |
| **Média ponderada** | **0,40** | 0,2550 | 27,240 | 14,08% |
| Mediana | 0,35 | 0,2532 | **27,235** | **14,16%** |
| Mínimo | 0,25 | **0,2572** | 27,633 | 9,18% |

A escolha foi **média ponderada com `τ = 0,40`**, preservando **97,24% do AP** na calibração.

### Efeito do limiar — slide 14 (calibração)

Configuração **2B**, média ponderada, camada 61:

| `τ` | COCO AP | GMAC | % EE | AP preservado | AP/GMAC |
|--:|--:|--:|--:|--:|--:|
| 0,20 | 0,2049 | **23,221** | **64,70%** | 78,16% | 0,008826 |
| 0,30 | 0,2385 | 25,822 | 31,88% | 90,96% | 0,009236 |
| 0,35 | 0,2498 | 26,713 | 20,68% | 95,27% | 0,009352 |
| **0,40** | **0,2550** | **27,240** | **14,08%** | **97,24%** | **0,009360** |
| 0,45 | 0,2585 | 27,635 | 9,14% | 98,60% | 0,009355 |
| 0,50 | 0,2601 | 27,830 | 6,70% | 99,19% | 0,009346 |

Quanto menor o limiar, mais imagens saem cedo e menor é o custo, mas maior pode ser a perda de AP.

![Efeito do limiar na calibração](figures/threshold_tradeoff.svg)

### Comparação final — slides 15, 16 e 18

| Modelo | AP AdaCon | AP com EE | AP preservado | GMAC AdaCon | GMAC com EE | Redução | % EE |
|:--|--:|--:|--:|--:|--:|--:|--:|
| **2B** | 0,2546 | **0,2491** | **97,83%** | 28,039 | 27,187 | 3,04% | 14,00% |
| **3B** | 0,2331 | 0,2278 | 97,73% | 27,169 | 25,952 | **4,48%** | 20,94% |
| **4B** | 0,2268 | 0,2217 | 97,74% | 26,735 | **25,610** | 4,21% | 20,94% |

Em todos os modelos, foi utilizada **média ponderada**. O limiar foi **0,40 no 2B** e **0,35 nos modelos 3B e 4B**.

A configuração recomendada foi **2B + saída na camada 61 + média ponderada + `τ = 0,40`**, por ter o maior AP final. Ela reduziu **0,852 GMAC por imagem (3,04%)**, preservando **97,83% do AP**. O **3B** teve a maior redução relativa de GMAC; o **4B**, o menor GMAC absoluto.

![AdaCon original e AdaCon com saída antecipada](figures/model_comparison.svg)

**Nota sobre os percentuais:** os valores de AP preservado são os publicados nos slides. Como o AP mostrado está arredondado para quatro casas, recalcular a razão a partir dessa tabela pode produzir diferença de aproximadamente 0,01 ponto percentual.

**Calibração e validação são etapas distintas.** Por isso, os valores do ajuste de limiar (AP 0,2550; GMAC 27,240) diferem dos resultados de validação final para 2B (AP 0,2491; GMAC 27,187).

### Análise das imagens antecipadas — slide 17

No modelo 2B, **700 das 5.000 imagens (14,00%)** encerraram cedo o processamento. Essas imagens tinham, em média, **5,52 objetos e 2,42 classes**, contra **7,55 objetos e 3,01 classes** nas demais.

Algumas classes apareceram mais frequentemente em cenas que saíram cedo: **esquis (45,00%)**, **snowboard (42,86%)** e **zebra (37,65%)**. Isso não significa necessariamente maior precisão: esquis, por exemplo, tiveram **4,67% de AP** no subconjunto antecipado. A taxa de saída e a qualidade da detecção devem ser interpretadas separadamente.

A fonte destas tabelas é a [apresentação final do SIAC](docs/apresentacao_siac_2026.pptx).

## Como executar

### 1. Reproduzir a análise das tabelas e dos gráficos

O processamento dos resultados já registrados funciona com **Python 3.9+ e biblioteca padrão**, sem precisar do COCO ou de pesos de rede neural.

Clone o projeto (o GitHub exige acesso, pois este repositório é privado):

```bash
git clone https://github.com/PedroCintra67/Adacon_Early_Exit.git
cd Adacon_Early_Exit
```

Confira as métricas transcritas:

```bash
python scripts/validate_results.py
```

Recrie os dois gráficos SVG em `figures/`:

```bash
python scripts/plot_results.py
```

Os dados estão em `results/*.csv`, e os gráficos podem ser abertos no navegador ou vistos diretamente no GitHub. Esses comandos **verificam os resultados documentados**, sem executar novamente as redes.

### 2. Executar o AdaCon original

O código-base está em `baseline/adacon/`. Para uma execução de inferência, é preciso instalar as dependências do projeto original, obter seus pesos e fornecer uma imagem.

```bash
cd baseline/adacon
python -m venv .venv
```

Ative o ambiente: no PowerShell, `.venv\Scripts\Activate.ps1`; em Linux/macOS, `source .venv/bin/activate`. Depois:

```bash
python -m pip install -r requirements.txt
```

Com **Bash, wget e conexão à internet**, baixe os pesos da arquitetura original:

```bash
bash weights/download_adacon_weights.sh
```

Verifique os caminhos dos arquivos no `model.args` e execute a inferência sobre uma imagem local:

```bash
python detect.py --adaptive --model model.args --source caminho/da/imagem.jpg --img-size 416
```

Este exemplo utiliza **AdaCon original de quatro ramos**. As versões e os pesos desse projeto da literatura são legados; essa instalação e a inferência não foram executadas nesta preparação.

### 3. Preparar o COCO e refazer o estudo

Para avaliar a base no COCO, baixe as imagens e anotações oficiais, prepare os caminhos usados em `baseline/adacon/data/coco2017.data` e verifique os pesos descritos em `model.args`. Com o ambiente devidamente configurado, o script de avaliação original aceita:

```bash
python test.py --adaptive --model model.args --data data/coco2017.data --img-size 416
```

Para obter novamente os resultados **da pesquisa com saídas antecipadas**, o fluxo experimental é:

1. Recuperar o mesmo particionamento de **113.287 imagens de treino, 5.000 de calibração e 5.000 de validação**.
2. Preparar os modelos **2B, 3B e 4B** e seus pesos.
3. Integrar e treinar as saídas nas camadas **49, 52, 55, 58 e 61**.
4. Calibrar o método de decisão e os limiares **0,00–1,00** (passo **0,05**).
5. Avaliar COCO AP, GMAC por rota e taxa de saída antecipada; comparar com cada modelo sem saída.

**Disponibilidade do código experimental:** os arquivos usados para montar este repositório incluíam a base pública AdaCon, os slides e as tabelas, mas **não continham a implementação das saídas antecipadas, seus checkpoints, os logs nem a lista exata de calibração**. Portanto, os comandos acima permitem recriar a **análise dos resultados** e servem de referência para executar a **arquitetura-base**, mas ainda não reproduzem os experimentos de *early exit* a partir das imagens. Não há um comando de treino ou inferência dessa extensão para executar até que tais arquivos sejam recuperados.

## Organização

```text
Adacon_Early_Exit/
├── baseline/adacon/    # código original AdaCon e configurações
├── docs/               # apresentação SIAC e procedência
├── figures/            # visualizações dos dados
├── results/            # resultados em CSV
├── scripts/            # validação e gráficos
├── .gitignore
├── LICENSE
└── README.md
```

## Referências e créditos

- M. Neseem e S. Reda, *AdaCon: Adaptive Context-Aware Object Detection for Resource-Constrained Embedded Devices*, ICCAD 2021. [Artigo](https://arxiv.org/abs/2108.06850) · [Código original](https://github.com/scale-lab/AdaCon).
- S. Teerapittayanon, B. McDanel e H. T. Kung, *BranchyNet: Fast Inference via Early Exiting from Deep Neural Networks*, ICPR 2016.
- T.-Y. Lin et al., *Microsoft COCO: Common Objects in Context*, ECCV 2014.

O recorte do código AdaCon em `baseline/adacon/` mantém sua **licença GPL-3.0** e a atribuição aos autores originais. A [documentação de procedência](docs/PROVENIENCIA.md) detalha a origem dos arquivos.
