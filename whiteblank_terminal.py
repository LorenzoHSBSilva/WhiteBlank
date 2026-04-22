from abc import ABC, abstractmethod
from functools import singledispatch
from typing import Optional


@singledispatch
def adicionar_ao_slide(elemento, slide):
    print(f"  ✗ Tipo '{type(elemento).__name__}' não suportado.")


class ElementoGrafico(ABC):
    def __init__(self, largura: int, altura: int):
        self.largura = largura
        self.altura  = altura

    @abstractmethod
    def alterar_proporcoes(self, nova_largura: int, nova_altura: int):
        pass

    @abstractmethod
    def renderizar(self) -> str:
        pass

    def info(self) -> str:
        return f"[{self.__class__.__name__}] {self.largura}x{self.altura}px"


class Texto(ElementoGrafico):
    def __init__(self, conteudo: str, fonte: str = "Arial",
                 tamanho_fonte: int = 16, cor: str = "preto",
                 largura: int = 200, altura: int = 50):
        super().__init__(largura, altura)
        self.conteudo      = conteudo
        self.fonte         = fonte
        self.tamanho_fonte = tamanho_fonte
        self.cor           = cor

    def alterar_proporcoes(self, nova_largura: int, nova_altura: int):
        escala = nova_altura / self.altura if self.altura else 1
        self.tamanho_fonte = max(8, int(self.tamanho_fonte * escala))
        self.largura, self.altura = nova_largura, nova_altura
        print(f"  ✏  Texto redimensionado → {nova_largura}x{nova_altura}, fonte: {self.tamanho_fonte}pt")

    def renderizar(self) -> str:
        b = "─" * (len(self.conteudo) + 4)
        return (f"  ┌{b}┐\n"
                f"  │  {self.conteudo}  │  [{self.fonte}, {self.tamanho_fonte}pt, {self.cor}]\n"
                f"  └{b}┘")


class Imagem(ElementoGrafico):
    def __init__(self, nome_arquivo: str, largura: int = 200, altura: int = 150):
        super().__init__(largura, altura)
        self.nome_arquivo = nome_arquivo
        self.proporcao    = largura / altura if altura else 1

    def alterar_proporcoes(self, nova_largura: int, nova_altura: int):
        nova_prop = nova_largura / nova_altura if nova_altura else 1
        aviso = f" ⚠ distorção ({self.proporcao:.2f}→{nova_prop:.2f})" if abs(nova_prop - self.proporcao) > 0.1 else ""
        self.largura, self.altura = nova_largura, nova_altura
        print(f"  🖼  Imagem redimensionada → {nova_largura}x{nova_altura}{aviso}")

    def renderizar(self) -> str:
        w = max(20, min(self.largura // 10, 36))
        return (f"  ╔{'═'*w}╗\n"
                f"  ║{'🖼  ' + self.nome_arquivo:^{w}}║\n"
                f"  ║{f'{self.largura}x{self.altura}px':^{w}}║\n"
                f"  ╚{'═'*w}╝")


@adicionar_ao_slide.register(Texto)
def _(elemento: Texto, slide):
    slide.elementos.append(elemento)
    print(f"  + Texto '{elemento.conteudo[:25]}' adicionado ao Slide {slide.ordem}")

@adicionar_ao_slide.register(Imagem)
def _(elemento: Imagem, slide):
    slide.elementos.append(elemento)
    print(f"  + Imagem '{elemento.nome_arquivo}' adicionada ao Slide {slide.ordem}")


def buscar_elemento(slide, chave):
    if isinstance(chave, int):
        if 0 <= chave < len(slide.elementos):
            el = slide.elementos[chave]
            print(f"  🔍 [{chave}]: {el.info()}")
            return el
        print(f"  ✗ Índice fora do intervalo.")
    elif isinstance(chave, str):
        for el in slide.elementos:
            ref = el.conteudo if isinstance(el, Texto) else el.nome_arquivo
            if chave.lower() in ref.lower():
                print(f"  🔍 '{chave}': {el.info()}")
                return el
        print(f"  ✗ Nenhum elemento contém '{chave}'.")
    return None


class Template:
    def __init__(self, nome: str, elementos: list, criador: 'Usuario'):
        self.nome      = nome
        self.elementos = elementos
        self.criador   = criador
        self.estado    = "privado"

    def publicar(self):
        self.estado = "publicado"
        print(f"  ✓ Template '{self.nome}' publicado!")

    def info(self):
        print(f"  {self.nome} [{self.estado}] — {self.criador.email} — {len(self.elementos)} elemento(s)")


class Slide:
    def __init__(self, ordem: int):
        self.ordem     = ordem
        self.elementos: list[ElementoGrafico] = []

    def adicionar_elemento(self, elemento: ElementoGrafico):
        adicionar_ao_slide(elemento, self)

    def remover_elemento(self, indice: int):
        if 0 <= indice < len(self.elementos):
            print(f"  - Removido: {self.elementos.pop(indice).info()}")
        else:
            print("  ✗ Índice inválido.")

    def limpar(self):
        self.elementos.clear()
        print(f"  Slide {self.ordem} limpo.")

    def salvar_como_template(self, nome: str, criador: 'Usuario') -> Template:
        dados = []
        for el in self.elementos:
            if isinstance(el, Texto):
                dados.append({"tipo": "texto", "conteudo": el.conteudo, "fonte": el.fonte,
                               "tamanho_fonte": el.tamanho_fonte, "cor": el.cor,
                               "largura": el.largura, "altura": el.altura})
            elif isinstance(el, Imagem):
                dados.append({"tipo": "imagem", "nome_arquivo": el.nome_arquivo,
                               "largura": el.largura, "altura": el.altura})
        t = Template(nome, dados, criador)
        print(f"  ✓ Template '{nome}' criado com {len(dados)} elemento(s).")
        return t

    def aplicar_template(self, template: Template):
        for d in template.elementos:
            el = (Texto(d["conteudo"], d.get("fonte","Arial"), d.get("tamanho_fonte",16),
                        d.get("cor","preto"), d.get("largura",200), d.get("altura",50))
                  if d["tipo"] == "texto"
                  else Imagem(d["nome_arquivo"], d.get("largura",200), d.get("altura",150)))
            self.adicionar_elemento(el)
        print(f"  ✓ Template '{template.nome}' aplicado.")

    def renderizar(self):
        print(f"\n  ┌──────────────────────────────────────┐")
        print(f"  │  SLIDE {self.ordem}  ({len(self.elementos)} elemento(s))               │")
        print(f"  └──────────────────────────────────────┘")
        if not self.elementos:
            print("  (vazio)")
            return
        for i, el in enumerate(self.elementos):
            print(f"\n  [{i}] {el.info()}")
            print(el.renderizar())


class Projeto:
    def __init__(self, nome: str, dono: 'Usuario'):
        self.nome    = nome
        self.dono    = dono
        self.slides: list[Slide]      = [Slide(ordem=1)]
        self.membros: list['Usuario'] = [dono]

    def adicionar_slide(self) -> Slide:
        s = Slide(len(self.slides) + 1)
        self.slides.append(s)
        print(f"  + Slide {s.ordem} adicionado.")
        return s

    def remover_slide(self, idx: int):
        if len(self.slides) <= 1:
            print("  ✗ Projeto precisa ter pelo menos 1 slide.")
        elif 0 <= idx < len(self.slides):
            s = self.slides.pop(idx)
            for i, sl in enumerate(self.slides): sl.ordem = i + 1
            print(f"  - Slide {s.ordem} removido.")
        else:
            print("  ✗ Índice inválido.")

    def adicionar_membro(self, usuario: 'Usuario'):
        if usuario in self.membros:
            print(f"  ✗ {usuario.email} já é membro.")
        else:
            self.membros.append(usuario)
            print(f"  + {usuario.email} adicionado.")

    def remover_membro(self, usuario: 'Usuario'):
        if usuario is self.dono:
            print("  ✗ O dono não pode ser removido.")
        elif usuario in self.membros:
            self.membros.remove(usuario)
            print(f"  - {usuario.email} removido.")
        else:
            print(f"  ✗ {usuario.email} não é membro.")

    def info(self):
        print(f"\n  Projeto : {self.nome}")
        print(f"  Dono    : {self.dono.email}")
        print(f"  Slides  : {len(self.slides)}")
        print(f"  Membros : {', '.join(m.email for m in self.membros)}")


class Usuario:
    def __init__(self, email: str, senha: str):
        self.email         = email
        self.senha         = senha
        self.status        = "Deslogado"
        self.biografia     = ""
        self.foto_perfil   = None
        self.modo_restrito = False
        self.projetos:  list[Projeto]  = []
        self.templates: list[Template] = []

    def login(self, senha: str) -> bool:
        if self.senha == senha:
            self.status = "Logado"
            print(f"  ✓ {self.email} logado.")
            return True
        print("  ✗ Senha incorreta.")
        return False

    def logout(self):
        self.status = "Deslogado"
        print(f"  {self.email} deslogado.")

    def atualizar_perfil(self, biografia: Optional[str] = None,
                         foto: Optional[str] = None,
                         modo_restrito: Optional[bool] = None):
        if biografia    is not None: self.biografia     = biografia;    print("  ✓ Biografia atualizada.")
        if foto         is not None: self.foto_perfil   = foto;         print(f"  ✓ Foto: '{foto}'")
        if modo_restrito is not None: self.modo_restrito = modo_restrito; print(f"  ✓ Modo restrito: {'on' if modo_restrito else 'off'}")

    def criar_projeto(self, nome: str) -> Projeto:
        p = Projeto(nome, self)
        self.projetos.append(p)
        print(f"  ✓ Projeto '{nome}' criado!")
        return p

    def info(self):
        print(f"\n  Email    : {self.email} [{self.status}]")
        print(f"  Biografia: {self.biografia or '(vazia)'}")
        print(f"  Foto     : {self.foto_perfil or '(nenhuma)'}")
        print(f"  Restrito : {'Sim' if self.modo_restrito else 'Não'}")
        print(f"  Projetos : {len(self.projetos)}")
        print(f"  Templates: {len(self.templates)}")


biblioteca_global: list[Template] = []

def publicar_na_biblioteca(t: Template):
    t.publicar()
    if t not in biblioteca_global:
        biblioteca_global.append(t)

def listar_biblioteca():
    if not biblioteca_global:
        print("  (biblioteca vazia)")
    else:
        for i, t in enumerate(biblioteca_global):
            print(f"  [{i}] {t.nome} — {t.criador.email} ({len(t.elementos)} elem.)")


def L(char="─", n=50): print(char * n)
def cab(titulo): print(); L("═"); print(f"  {titulo}"); L("═")


def run():
    usuarios: dict[str, Usuario] = {}
    u: Optional[Usuario] = None
    proj: Optional[Projeto] = None
    slide: Optional[Slide] = None

    while True:
        cab("WHITEBLANK")
        print(f"  Usuário : {u.email + ' (' + u.status + ')' if u else 'não logado'}")
        print(f"  Projeto : {proj.nome if proj else '—'}")
        print(f"  Slide   : {slide.ordem if slide else '—'}")
        L("-")

        if not u:
            print("  1. Cadastrar  2. Login  0. Sair")
        else:
            print("  PROJETO  1.Criar  2.Selecionar  22.Info")
            print("  MEMBROS  3.Add    4.Remover      5.Ver")
            print("  SLIDES   6.Add    7.Selecionar   8.Remover")
            print("  ELEM.    9.Texto  10.Imagem  11.Buscar  12.Redim.  13.Remover  14.Ver")
            print("  TEMPLAT  15.Salvar  16.Aplicar  17.Meus  18.Publicar  19.Biblioteca")
            print("  PERFIL   20.Editar  21.Ver")
            print("  L.Logout  0.Sair")

        L()
        op = input("  Escolha: ").strip().upper()

        if op == "0":
            print("\n  Até logo!\n"); break

        elif not u:
            if op == "1":
                e, s = input("  Email: ").strip(), input("  Senha: ").strip()
                if e in usuarios: print("  ✗ Email já cadastrado.")
                else: usuarios[e] = Usuario(e, s); print(f"  ✓ '{e}' criado!")
            elif op == "2":
                e, s = input("  Email: ").strip(), input("  Senha: ").strip()
                usr = usuarios.get(e)
                if usr and usr.login(s): u = usr
                else: print("  ✗ Email ou senha incorretos.")

        else:
            if op == "1":
                nome = input("  Nome do projeto: ").strip()
                proj = u.criar_projeto(nome); slide = proj.slides[0]

            elif op == "2":
                if not u.projetos: print("  Nenhum projeto.")
                else:
                    [print(f"  [{i}] {p.nome}") for i, p in enumerate(u.projetos)]
                    idx = input("  Número: ").strip()
                    if idx.isdigit() and int(idx) < len(u.projetos):
                        proj = u.projetos[int(idx)]; slide = proj.slides[0]
                        print(f"  ✓ '{proj.nome}' selecionado.")

            elif op == "3":
                if not proj: print("  ✗ Selecione um projeto.")
                else:
                    e = input("  Email do membro: ").strip()
                    proj.adicionar_membro(usuarios[e]) if e in usuarios else print(f"  ✗ '{e}' não cadastrado.")

            elif op == "4":
                if not proj: print("  ✗ Selecione um projeto.")
                else:
                    [print(f"  [{i}] {m.email}{' (dono)' if m is proj.dono else ''}") for i, m in enumerate(proj.membros)]
                    idx = input("  Índice: ").strip()
                    if idx.isdigit() and int(idx) < len(proj.membros):
                        proj.remover_membro(proj.membros[int(idx)])

            elif op == "5":
                if not proj: print("  ✗ Selecione um projeto.")
                else: [print(f"    • {m.email}{' ★' if m is proj.dono else ''}") for m in proj.membros]

            elif op == "6":
                if not proj: print("  ✗ Selecione um projeto.")
                else: slide = proj.adicionar_slide()

            elif op == "7":
                if not proj: print("  ✗ Selecione um projeto.")
                else:
                    [print(f"  [{i}] Slide {s.ordem} ({len(s.elementos)} elem.)") for i, s in enumerate(proj.slides)]
                    idx = input("  Número: ").strip()
                    if idx.isdigit() and int(idx) < len(proj.slides):
                        slide = proj.slides[int(idx)]; print(f"  ✓ Slide {slide.ordem}.")

            elif op == "8":
                if not proj: print("  ✗ Selecione um projeto.")
                else:
                    [print(f"  [{i}] Slide {s.ordem}") for i, s in enumerate(proj.slides)]
                    idx = input("  Índice: ").strip()
                    if idx.isdigit():
                        proj.remover_slide(int(idx))
                        slide = proj.slides[0] if proj.slides else None

            elif op == "9":
                if not slide: print("  ✗ Selecione um slide.")
                else:
                    c = input("  Texto: ").strip()
                    f = input("  Fonte (Enter=Arial): ").strip() or "Arial"
                    t = input("  Tamanho (Enter=16): ").strip()
                    slide.adicionar_elemento(Texto(c, f, int(t) if t.isdigit() else 16))

            elif op == "10":
                if not slide: print("  ✗ Selecione um slide.")
                else:
                    n = input("  Nome do arquivo: ").strip()
                    l = input("  Largura (Enter=200): ").strip()
                    a = input("  Altura (Enter=150): ").strip()
                    slide.adicionar_elemento(Imagem(n, int(l) if l.isdigit() else 200, int(a) if a.isdigit() else 150))

            elif op == "11":
                if not slide or not slide.elementos: print("  ✗ Slide vazio.")
                else:
                    slide.renderizar()
                    c = input("  Buscar por índice ou palavra: ").strip()
                    buscar_elemento(slide, int(c) if c.isdigit() else c)

            elif op == "12":
                if not slide or not slide.elementos: print("  ✗ Slide vazio.")
                else:
                    slide.renderizar()
                    idx = input("  Índice: ").strip()
                    l   = input("  Nova largura: ").strip()
                    a   = input("  Nova altura : ").strip()
                    if idx.isdigit() and l.isdigit() and a.isdigit():
                        slide.elementos[int(idx)].alterar_proporcoes(int(l), int(a))

            elif op == "13":
                if not slide or not slide.elementos: print("  ✗ Slide vazio.")
                else:
                    slide.renderizar()
                    idx = input("  Índice: ").strip()
                    if idx.isdigit(): slide.remover_elemento(int(idx))

            elif op == "14":
                if slide: slide.renderizar()
                else: print("  ✗ Selecione um slide.")

            elif op == "15":
                if not slide or not slide.elementos: print("  ✗ Slide vazio.")
                else:
                    n = input("  Nome do template: ").strip()
                    if n:
                        tmpl = slide.salvar_como_template(n, u)
                        u.templates.append(tmpl)

            elif op == "16":
                todos = list({id(t): t for t in u.templates + biblioteca_global}.values())
                if not todos: print("  ✗ Sem templates disponíveis.")
                elif not slide: print("  ✗ Selecione um slide.")
                else:
                    [print(f"  [{i}] {t.nome} [{t.estado}]") for i, t in enumerate(todos)]
                    idx = input("  Número: ").strip()
                    if idx.isdigit() and int(idx) < len(todos):
                        slide.aplicar_template(todos[int(idx)])

            elif op == "17":
                if not u.templates: print("  Sem templates.")
                else: [t.info() for t in u.templates]

            elif op == "18":
                if not u.templates: print("  ✗ Sem templates.")
                else:
                    [print(f"  [{i}] {t.nome} [{t.estado}]") for i, t in enumerate(u.templates)]
                    idx = input("  Número: ").strip()
                    if idx.isdigit() and int(idx) < len(u.templates):
                        publicar_na_biblioteca(u.templates[int(idx)])

            elif op == "19":
                listar_biblioteca()

            elif op == "20":
                print("  (Enter para não alterar)")
                bio  = input("  Biografia: ").strip() or None
                foto = input("  Foto      : ").strip() or None
                r    = input("  Restrito (s/n/Enter): ").strip().lower()
                u.atualizar_perfil(bio, foto, True if r=='s' else (False if r=='n' else None))

            elif op == "21":
                u.info()

            elif op == "22":
                if proj: proj.info()
                else: print("  ✗ Selecione um projeto.")

            elif op == "L":
                u.logout(); u = proj = slide = None

        input("\n  [Enter]")


if __name__ == "__main__":
    run()
