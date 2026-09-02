# Documento complementar — MOD-1 (Fábrica e Detecção)

ODS 2026/2 · versão 4 do detalhamento de atividades · squad Biblioteca

## 1. Escopo e responsabilidade

MOD-1 possui dois componentes, cada um com dono único:

| Componente | Camada | Missão |
|---|---|---|
| B5 — Fábrica de artefatos | Coluna transversal | Produzir e publicar, com procedência, todo artefato de modelo que um componente carrega |
| I1 — Detecção por quadro | Camada 2 · Inferência | Dizer o que há no quadro, com caixa, classe e confiança |

**Fronteira explícita**: o conteúdo do dataset (imagens, critério de rotulagem, taxonomia de classes) pertence à aplicação que o encomendou. MOD-1 é dono da ferramenta, da disciplina de execução e do código do detector, não do conteúdo.

## 2. Atividades e pesos

### B5 (peso total: 11)
| Peso | Atividade | Entregável |
|---|---|---|
| 1 | Coleta e anotação de dataset | Ferramenta configurada + dataset anotado por aplicação |
| 2 | Treino e avaliação | Modelo treinado + métrica sobre conjunto de avaliação separado |
| 1 | Registro e versionamento | Identificador de versão propagado em todo evento |
| 3 | Conversão e otimização | Modelo ONNX/TensorRT + relatório de custo de acurácia (FP16/INT8) |
| 2 | Contrato ONNX | Interface publicada + modelo de exemplo + latência medida |
| 2 | Publicação para o runtime | Artefato no formato consumido por P2 |

### I1 (peso total: 5)
| Peso | Atividade | Entregável |
|---|---|---|
| 2 | Detector multi-classe (pessoa, veículo, bola, peça, produto) | Detector único, parametrizado por artefato |
| 1 | Saída padronizada (caixa, classe, confiança) | Contrato de dados alinhado com B1 |
| 2 | Separação artefato/componente | Garantia de que trocar artefato não exige trocar código |

Peso total do squad: 16 pontos / 9 atividades / 3 pessoas ≈ 5,3 por pessoa.

## 3. Interfaces com outros componentes

| Componente | Direção | O que é trocado |
|---|---|---|
| B1 (contratos de evento) | consome de MOD-1 | Esquema de saída do detector (caixa, classe, confiança) |
| B3 (proveniência) | MOD-1 alimenta | Versão do artefato em todo evento produzido |
| B4 (contratos executáveis / CI) | MOD-1 expõe | Conjunto de avaliação e mock de saída para a suíte de contrato |
| P2 (runtime de aceleração) | MOD-1 publica | Artefato convertido, dentro do orçamento de memória da placa |
| Squads de aplicação (A1, A3, A4, A5, A6, A7, A8) | recebem de MOD-1 | Fornecem dados brutos e critério de rotulagem; recebem artefato treinado |

## 4. Casos especiais

- **Léxico de Libras (A6)**: não é treinado — é capturado por I4 (fora do MOD-1) em modo captura, corrigido à mão, e apenas registrado/versionado por B5 como qualquer outro artefato.
- **Objetos pequenos e rápidos** (ex. bola em A4): caso reconhecidamente difícil dentro de I1, não deve ser tratado como classe comum — merece atenção própria no plano de dataset e avaliação.

## 5. Plano de entregas sugerido (a validar com o squad)

1. **Ciclo 1** — ferramenta de anotação no ar; formato de `manifest.json` fechado; contrato de saída do detector (caixa/classe/confiança) proposto a B1.
2. **Ciclo 2** — pipeline de treino genérico funcionando ponta a ponta com um dataset piloto; primeira versão de I1 publicada para P2.
3. **Ciclo 3** — conversão ONNX/TensorRT validada na placa com latência medida; suíte de avaliação exposta a B4.
4. **Ciclo 4** — publicação recorrente para as aplicações que dependem de I1 (A1, A2, A3, A5, A7, A8); ajustes de memória/orçamento com P2.

## 6. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Guia de rotulagem atrasado pelas aplicações | Bloqueia anotação | Prazo combinado na primeira reunião entre squads |
| Modelos não cabem nos 8 GB compartilhados da Jetson | Falha em produção, não em teste | Medir consumo por modelo cedo, decidir o que fica residente com P2 |
| Perda de acurácia na conversão FP16/INT8 | Detecção degradada sem sintoma óbvio | Medir custo com dados reais antes de publicar |
| Objeto pequeno/rápido tratado como classe comum | Baixa qualidade de detecção sem alerta | Tratamento e avaliação dedicados dentro de I1 |

## 7. Glossário rápido

- **Artefato**: modelo, pesos ou dado versionado que pertence à aplicação, mesmo quando produzido por MOD-1.
- **Componente**: unidade de código com dono único (B5 ou I1), independente do artefato que carrega.
- **Manifest**: arquivo que descreve origem, critério e integridade de uma versão de dataset ou de um run de treino.
