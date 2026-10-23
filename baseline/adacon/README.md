# AdaCon: código-base da literatura

Recorte do repositório público [scale-lab/AdaCon](https://github.com/scale-lab/AdaCon), commit `cb8b871` (07/04/2023), sob **GPL-3.0**. Este diretório reúne os módulos de detecção e treinamento e as configurações de 4 ramos usadas como referência. O código original também deriva de componentes do YOLOv3/Ultralytics.

Foi incluído para contextualizar a arquitetura sobre a qual o estudo do GTA/UFRJ propôs saídas antecipadas. **O código desta pasta, por si só, não implementa a extensão de early exit apresentada nos resultados.**

Para trabalhar com a base, a partir desta pasta:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Os pesos do AdaCon podem ser obtidos pelo script original `weights/download_adacon_weights.sh` (requer Bash e conexão de rede). O COCO 2017 também precisa ser baixado separadamente. Depois de configurar os caminhos, o comando de inferência do AdaCon original é:

```bash
python detect.py --model model.args --adaptive --source imagem.jpg
```

> Esses comandos foram documentados a partir da base original, mas não foram executados nesta preparação: os pesos e o dataset não estão incluídos, e o ambiente PyTorch legado pode exigir ajustes de versão.

Para os resultados do trabalho de iniciação científica, consulte o [`README` principal](../../README.md) e as [notas de procedência](../../docs/PROVENIENCIA.md).
