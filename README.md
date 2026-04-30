# WhiteBlank 🖼️

> Editor de slides colaborativo desenvolvido como alternativa ao Canva, focado em leveza, estabilidade e originalidade.  
> **Aluno:** Lorenzo Holanda Sodré De Brito Silva

---

## 📋 Sumário

1. [Como executar](#como-executar)
2. [Estrutura dos arquivos](#estrutura-dos-arquivos)
3. [Diagrama de classes](#diagrama-de-classes)
4. [Herança e Polimorfismo](#herança-e-polimorfismo)
5. [Propósito de cada classe](#propósito-de-cada-classe)
6. [Funcionalidades implementadas](#funcionalidades-implementadas)

---

## Como executar

### Passos

```bash
# Clone o repositório
git clone <url-do-repositório>
cd whiteblank

# Não há dependências externas — rode direto:
python main.py
```

O programa roda no terminal com um **menu interativo**. Basta digitar o número/letra da opção desejada e pressionar Enter.

### Navegação rápida pelo menu

| Estado | Ações disponíveis |
|--------|-------------------|
| Deslogado | Cadastrar conta (`1`), fazer login (`2`) |
| Logado | Gerenciar perfil, amigos, projetos, slides, elementos e templates |

---

## Estrutura dos arquivos

```
whiteblank/
│
├── main.py        # Ponto de entrada — loop de menu e interface com o usuário
├── usuario.py     # Classe Usuario + biblioteca global de templates
├── modelos.py     # Classes Projeto, Slide e Template
└── elementos.py   # Hierarquia de elementos gráficos (ElementoGrafico, Texto, Imagem)
```

---

## Diagrama de classes

```
          ┌──────────────────────┐
          │   ElementoGrafico    │  ← Classe abstrata (ABC)
          │ ─────────────────── │
          │ + largura: int       │
          │ + altura: int        │
          │ ─────────────────── │
          │ + info() -> str      │
          │ @ alterar_proporcoes │  ← método abstrato
          │ @ renderizar()       │  ← método abstrato
          └──────────┬───────────┘
                     │  herança
           ┌─────────┴──────────┐
           │                    │
  ┌────────▼───────┐   ┌────────▼───────┐
  │     Texto      │   │    Imagem      │
  │ ────────────── │   │ ────────────── │
  │ + conteudo     │   │ + nome         │
  │ + fonte        │   │ + proporcao    │
  │ + tamanho      │   │ ────────────── │
  │ + cor          │   │ alterar_prop.. │  ← polimorfismo
  │ ────────────── │   │ renderizar()   │  ← polimorfismo
  │ alterar_prop.. │   └────────────────┘
  │ renderizar()   │
  └────────────────┘

  ┌────────────────┐        ┌──────────────────┐
  │    Template    │        │      Slide       │
  │ ─────────────  │        │ ──────────────── │
  │ + nome         │        │ + ordem: int     │
  │ + elementos    │◄───────│ + elementos[]    │
  │ + criador      │        │ ──────────────── │
  │ + estado       │        │ + adicionar_el.. │
  │ ────────────── │        │ + remover_el..   │
  │ + publicar()   │        │ + renderizar()   │
  │ + info()       │        │ + salvar_como_.. │
  └────────────────┘        │ + aplicar_templ  │
                            └────────┬─────────┘
                                     │ contido em
                            ┌────────▼─────────┐
                            │     Projeto      │
                            │ ──────────────── │
                            │ + nome           │
                            │ + dono: Usuario  │
                            │ + slides[]       │
                            │ + membros[]      │
                            │ ──────────────── │
                            │ + adicionar_sl.. │
                            │ + remover_slide  │
                            │ + adicionar_mem  │
                            └────────┬─────────┘
                                     │ pertence a
                            ┌────────▼─────────┐
                            │     Usuario      │
                            │ ──────────────── │
                            │ + email          │
                            │ + senha          │
                            │ + status         │
                            │ + projetos[]     │
                            │ + templates[]    │
                            │ + amigos[]       │
                            │ ──────────────── │
                            │ + login()        │
                            │ + logout()       │
                            │ + criar_projeto  │
                            │ + enviar_solic.. │
                            └──────────────────┘
```

---

## Herança e Polimorfismo

### Herança — `elementos.py`

A classe **`ElementoGrafico`** é uma **classe abstrata** (herda de `ABC`) que define o contrato comum para todo elemento que pode ser colocado em um slide.

```python
# elementos.py — linha 4
class ElementoGrafico(ABC):
    ...
    @abstractmethod
    def alterar_proporcoes(self, nova_largura: int, nova_altura: int):
        pass

    @abstractmethod
    def renderizar(self) -> str:
        pass
```

As classes **`Texto`** e **`Imagem`** herdam de `ElementoGrafico`:

```python
class Texto(ElementoGrafico):   # herda → deve implementar os 2 métodos abstratos
    ...

class Imagem(ElementoGrafico):  # herda → deve implementar os 2 métodos abstratos
    ...
```

Ambas chamam `super().__init__(largura, altura)` no construtor, reaproveitando os atributos da classe-pai.

---

### Polimorfismo — onde e como acontece

O polimorfismo ocorre sempre que o código trata um objeto como `ElementoGrafico` sem saber se é `Texto` ou `Imagem`, e cada subclasse responde de forma diferente ao mesmo método.

#### 1. `renderizar()` — comportamento diferente por tipo

| Classe | O que `renderizar()` faz |
|--------|--------------------------|
| `Texto` | Desenha uma caixa ASCII com o conteúdo, fonte e tamanho |
| `Imagem` | Desenha um quadro ASCII com `[IMG]` e as dimensões |

Usado em **`modelos.py → Slide.renderizar()`**:
```python
# modelos.py — linha 47
for i, el in enumerate(self.elementos):
    print(f"\n  [{i}] {el.info()}")
    print(el.renderizar())   # ← polimorfismo: Texto ou Imagem, sem if/else
```

#### 2. `alterar_proporcoes()` — lógica distinta por tipo

| Classe | O que `alterar_proporcoes()` faz |
|--------|----------------------------------|
| `Texto` | Recalcula o tamanho da fonte proporcionalmente à nova altura |
| `Imagem` | Atualiza dimensões e avisa se a proporção original foi distorcida |

Usado em **`main.py → opção "12"`**:
```python
# main.py — operação 12
slide.elementos[int(idx)].alterar_proporcoes(int(l), int(a))  # ← polimorfismo
```

#### 3. `isinstance()` — verificação de tipo quando necessária

Em alguns pontos do código, `isinstance` é usado para diferenciar `Texto` de `Imagem` quando o comportamento precisa ser distinto fora da hierarquia (ex: serializar para template, exibir label diferente):

```python
# modelos.py — Slide.adicionar_elemento()
label = el.conteudo[:25] if isinstance(el, Texto) else el.nome

# modelos.py — Slide.salvar_como_template()
if isinstance(el, Texto):
    dados.append({"tipo": "texto", ...})
else:
    dados.append({"tipo": "imagem", ...})
```

---

## Propósito de cada classe

### `elementos.py`

| Classe | Propósito |
|--------|-----------|
| `ElementoGrafico` | Classe base abstrata. Define a interface mínima que qualquer elemento visual deve ter: dimensões, `renderizar()` e `alterar_proporcoes()`. Garante que nenhuma instância direta seja criada. |
| `Texto` | Representa uma caixa de texto dentro de um slide. Armazena conteúdo, fonte, tamanho e cor. Implementa redimensionamento com escala de fonte proporcional. |
| `Imagem` | Representa uma imagem inserida no slide. Guarda nome do arquivo e proporção original, detectando distorções ao redimensionar. |

---

### `modelos.py`

| Classe | Propósito |
|--------|-----------|
| `Template` | Modelo reutilizável de slide. Armazena uma lista serializada de elementos (dicionários) e pode ser publicado na biblioteca da comunidade. Estados: `privado` ou `publicado`. |
| `Slide` | Unidade de edição do projeto. Contém uma lista de `ElementoGrafico` e oferece operações de adição, remoção, renderização, além de exportar/importar templates. |
| `Projeto` | Agrupa slides e membros. É o artefato principal criado por um usuário. Controla quem pode colaborar (lista de membros) e mantém a ordenação dos slides. |

---

### `usuario.py`

| Classe / Função | Propósito |
|-----------------|-----------|
| `Usuario` | Representa um usuário autenticado. Gerencia estado de login, perfil personalizável, lista de projetos, templates próprios e rede de amigos com sistema de solicitações. |
| `publicar_na_biblioteca()` | Função global que publica um template na biblioteca compartilhada da comunidade. |
| `listar_biblioteca()` | Função global que exibe todos os templates públicos disponíveis. |
| `biblioteca` | Lista global que funciona como repositório público de templates da comunidade. |

---

### `main.py`

| Elemento | Propósito |
|----------|-----------|
| `run()` | Loop principal da aplicação. Gerencia o estado global (`u`, `proj`, `slide`) e despacha cada opção do menu para os métodos das classes correspondentes. |
| `cabecalho()` | Renderiza o cabeçalho do menu com o contexto atual (usuário logado, projeto e slide selecionados). |

---

## Funcionalidades implementadas

As funcionalidades abaixo foram definidas no documento do projeto e estão mapeadas para o código:

### 2.1 — Editor de slides
Arrastar, redimensionar e rotacionar elementos; guias de alinhamento.

- **Redimensionar:** `ElementoGrafico.alterar_proporcoes()` → `elementos.py` (linhas 17 e 20), chamado via `main.py` opção `12`
- **Adicionar ao slide:** `Slide.adicionar_elemento()` → `modelos.py`
- **Remover do slide:** `Slide.remover_elemento()` → `modelos.py`

---

### 2.2 — Inserção e edição de texto
Adicionar caixas de texto; alterar fonte, tamanho, cor e alinhamento.

- **Classe responsável:** `Texto` → `elementos.py`
- **Inserção via menu:** `main.py` opção `9` (solicita conteúdo, fonte e tamanho)
- **Atributos:** `fonte`, `tamanho`, `cor` na classe `Texto`

---

### 2.3 — Upload e inserção de imagens
Upload, arrastar, redimensionar e cortar imagens.

- **Classe responsável:** `Imagem` → `elementos.py`
- **Inserção via menu:** `main.py` opção `10` (solicita nome do arquivo, largura e altura)
- **Redimensionamento com detecção de distorção:** `Imagem.alterar_proporcoes()` → `elementos.py`

---

### 2.4 — Usuário e login
Interface de autenticação com email, senha e perfil.

- **Classe responsável:** `Usuario` → `usuario.py`
- **Cadastro:** `main.py` opção `1` (deslogado) → cria instância de `Usuario`
- **Login/Logout:** `Usuario.login()` e `Usuario.logout()` → `usuario.py`
- **Edição de perfil** (biografia, foto, modo restrito): `Usuario.atualizar_perfil()` → `usuario.py`, chamado via `main.py` opção `E`

---

### 2.5 — Gerenciamento de slides
Adicionar, duplicar, deletar e reordenar slides.

- **Classe responsável:** `Projeto` → `modelos.py`
- **Adicionar slide:** `Projeto.adicionar_slide()` → `main.py` opção `6`
- **Remover slide:** `Projeto.remover_slide()` → `main.py` opção `8` (reordena automaticamente)
- **Selecionar slide:** `main.py` opção `7`

---

### 2.6 — Projetos em grupo
Utilização simultânea de mais de uma pessoa no mesmo projeto.

- **Classe responsável:** `Projeto` → `modelos.py` (atributo `membros`)
- **Adicionar membro:** `Projeto.adicionar_membro()` → `main.py` opção `3`
- **Remover membro:** `Projeto.remover_membro()` → `main.py` opção `4`
- **Ver membros:** `main.py` opção `5`
- **Restrição:** apenas amigos do dono podem ser adicionados como membros

---

### 2.7 — Criação de templates próprios
Criação de templates para maior personalização.

- **Classe responsável:** `Template` → `modelos.py`
- **Salvar slide como template:** `Slide.salvar_como_template()` → `main.py` opção `15`
- **Templates ficam em:** `Usuario.templates` (lista por usuário)

---

### 2.8 — Salvamento automático
Projetos mantidos salvos de forma nativa.

- **Implementado via:** estrutura em memória — objetos `Projeto` e `Slide` são mantidos na sessão enquanto o usuário está logado
- **Conceito mapeado:** `Conceito 3.9 — Salvamento` no documento do projeto

---

### 2.9 — Biblioteca da comunidade
Modelos feitos pela comunidade para uso de outros usuários.

- **Implementado em:** `usuario.py` — variável global `biblioteca: list[Template]`
- **Publicar template:** `publicar_na_biblioteca()` → `usuario.py`, chamado via `main.py` opção `18`
- **Listar biblioteca:** `listar_biblioteca()` → `usuario.py`, chamado via `main.py` opção `19`
- **Aplicar template da biblioteca:** `Slide.aplicar_template()` → `main.py` opção `16`

---

### 2.10 — Modo apresentação
Tela cheia, navegação entre slides e transição simples.

- **Implementado via:** `Slide.renderizar()` → `modelos.py`
- **Acesso via menu:** `main.py` opção `14` (renderiza o slide atual no terminal)
- **Renderização dos elementos:** cada elemento chama seu próprio `renderizar()` (polimorfismo), exibindo caixas ASCII formatadas

---

## Resumo de onde encontrar cada conceito do projeto

| Conceito (doc.) | Arquivo | Classe / Função |
|-----------------|---------|-----------------|
| 3.1 Autenticação e login | `usuario.py` | `Usuario.login()`, `Usuario.logout()` |
| 3.2 Template | `modelos.py` | `Template` |
| 3.3 Tela branca | `modelos.py` | `Slide` |
| 3.4 Gestão de slides | `modelos.py` | `Projeto` |
| 3.5 Grupo | `modelos.py` | `Projeto.membros` |
| 3.6 Link a usuários | `usuario.py` | `enviar_solicitacao()`, `aceitar_solicitacao()` |
| 3.7 Perfil personalizável | `usuario.py` | `Usuario.atualizar_perfil()` |
| 3.8 Arquivo (Texto/Imagem) | `elementos.py` | `Texto`, `Imagem` |
| 3.9 Salvamento | `modelos.py` | Objetos mantidos em memória na sessão |
| 3.10 Biblioteca de usuários | `usuario.py` | `biblioteca`, `publicar_na_biblioteca()` |
