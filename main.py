from typing import Optional
from elementos import Texto, Imagem
from modelos import Projeto, Slide
from usuario import Usuario, publicar_na_biblioteca, listar_biblioteca, biblioteca

MENU_DESLOGADO = "  1  Cadastrar        2  Login        0  Sair"

MENU_LOGADO = """\
  CONTA    L  Logout       P  Meu perfil    E  Editar perfil
  AMIGOS   A  Adicionar    B  Pedidos       C  Remover amigo   D  Ver amigos
  PROJETO  1  Criar        2  Selecionar    22 Info
  MEMBROS  3  Add membro   4  Rem. membro   5  Ver membros
  SLIDES   6  Add slide    7  Selecionar    8  Remover slide
  ELEM.    9  +Texto       10 +Imagem       11 Buscar
           12 Redim.       13 Remover       14 Ver slide
  TEMPL.   15 Salvar       16 Aplicar       17 Meus templ.
           18 Publicar     19 Biblioteca    0  Sair"""


def cabecalho(u, proj, slide):
    print()
    print("  " + "=" * 52)
    print(" " * 22 +  " WHITEBLANK")
    print("  " + "=" * 52)
    print(f"  Usuario : {u.email + ' (' + u.status + ')' if u else 'nao logado'}")
    print(f"  Projeto : {proj.nome if proj else '--'}")
    print(f"  Slide   : {slide.ordem if slide else '--'}")
    if u and u.pendentes:
        print(f"  * {len(u.pendentes)} solicitacao(oes) de amizade pendente(s)!")
    print("  " + "-" * 52)
    print(MENU_DESLOGADO if not u else MENU_LOGADO)
    print("  " + "-" * 52)


def run():
    usuarios: dict[str, Usuario] = {}
    u:     Optional[Usuario] = None
    proj:  Optional[Projeto] = None
    slide: Optional[Slide]   = None

    while True:
        cabecalho(u, proj, slide)
        op = input("  > ").strip().upper()

        if op == "0":
            print("\n  Ate logo!\n")
            break

        elif not u:
            if op == "1":
                e = input("  Email : ").strip()
                s = input("  Senha : ").strip()
                if e in usuarios:
                    print("  x Email ja cadastrado.")
                else:
                    usuarios[e] = Usuario(e, s)
                    print(f"  + Conta '{e}' criada!")
            elif op == "2":
                e = input("  Email : ").strip()
                s = input("  Senha : ").strip()
                usr = usuarios.get(e)
                if usr and usr.login(s):
                    u = usr
                else:
                    print("  x Email ou senha incorretos.")

        else:
            if op == "L":
                u.logout(); u = proj = slide = None

            elif op == "P":
                u.info()

            elif op == "E":
                print("  (Enter para nao alterar)")
                bio  = input("  Biografia : ").strip() or None
                foto = input("  Foto      : ").strip() or None
                r    = input("  Restrito (s/n): ").strip().lower()
                u.atualizar_perfil(bio, foto, True if r == "s" else (False if r == "n" else None))

            elif op == "A":
                e = input("  Email do usuario: ").strip()
                if e in usuarios:
                    u.enviar_solicitacao(usuarios[e])
                else:
                    print(f"  x '{e}' nao encontrado.")

            elif op == "B":
                if not u.pendentes:
                    print("  Nenhuma solicitacao pendente.")
                else:
                    for i, s_ in enumerate(u.pendentes):
                        print(f"  [{i}] {s_.email}")
                    idx = input("  Indice (aceitar) ou 'r <indice>' (recusar): ").strip()
                    if idx.startswith("r "):
                        i2 = idx[2:].strip()
                        if i2.isdigit() and int(i2) < len(u.pendentes):
                            u.recusar_solicitacao(u.pendentes[int(i2)])
                    elif idx.isdigit() and int(idx) < len(u.pendentes):
                        u.aceitar_solicitacao(u.pendentes[int(idx)])

            elif op == "C":
                if not u.amigos:
                    print("  Sem amigos cadastrados.")
                else:
                    for i, a in enumerate(u.amigos):
                        print(f"  [{i}] {a.email}")
                    idx = input("  Indice: ").strip()
                    if idx.isdigit() and int(idx) < len(u.amigos):
                        u.remover_amigo(u.amigos[int(idx)])

            elif op == "D":
                if not u.amigos:
                    print("  Sem amigos.")
                else:
                    for a in u.amigos:
                        print(f"  * {a.email}")

            elif op == "1":
                nome = input("  Nome do projeto: ").strip()
                proj = u.criar_projeto(nome)
                slide = proj.slides[0]

            elif op == "2":
                if not u.projetos:
                    print("  Nenhum projeto.")
                else:
                    for i, p in enumerate(u.projetos):
                        print(f"  [{i}] {p.nome}")
                    idx = input("  Numero: ").strip()
                    if idx.isdigit() and int(idx) < len(u.projetos):
                        proj = u.projetos[int(idx)]
                        slide = proj.slides[0]
                        print(f"  + '{proj.nome}' selecionado.")

            elif op == "22":
                if proj:
                    proj.info()
                else:
                    print("  x Selecione um projeto primeiro.")

            elif op == "3":
                if not proj:
                    print("  x Selecione um projeto primeiro.")
                else:
                    fora = [a for a in u.amigos if a not in proj.membros]
                    if not fora:
                        print("  Sem amigos disponíveis para adicionar.")
                    else:
                        for i, a in enumerate(fora):
                            print(f"  [{i}] {a.email}")
                        idx = input("  Indice: ").strip()
                        if idx.isdigit() and int(idx) < len(fora):
                            proj.adicionar_membro(fora[int(idx)])

            elif op == "4":
                if not proj:
                    print("  x Selecione um projeto primeiro.")
                else:
                    for i, m in enumerate(proj.membros):
                        print(f"  [{i}] {m.email}{' (dono)' if m is proj.dono else ''}")
                    idx = input("  Indice: ").strip()
                    if idx.isdigit() and int(idx) < len(proj.membros):
                        proj.remover_membro(proj.membros[int(idx)])

            elif op == "5":
                if not proj:
                    print("  x Selecione um projeto primeiro.")
                else:
                    for m in proj.membros:
                        print(f"  * {m.email}{' (dono)' if m is proj.dono else ''}")

            elif op == "6":
                if not proj:
                    print("  x Selecione um projeto primeiro.")
                else:
                    slide = proj.adicionar_slide()

            elif op == "7":
                if not proj:
                    print("  x Selecione um projeto primeiro.")
                else:
                    for i, s_ in enumerate(proj.slides):
                        print(f"  [{i}] Slide {s_.ordem} ({len(s_.elementos)} elem.)")
                    idx = input("  Numero: ").strip()
                    if idx.isdigit() and int(idx) < len(proj.slides):
                        slide = proj.slides[int(idx)]
                        print(f"  + Slide {slide.ordem} selecionado.")

            elif op == "8":
                if not proj:
                    print("  x Selecione um projeto primeiro.")
                else:
                    for i, s_ in enumerate(proj.slides):
                        print(f"  [{i}] Slide {s_.ordem}")
                    idx = input("  Indice: ").strip()
                    if idx.isdigit():
                        proj.remover_slide(int(idx))
                        slide = proj.slides[0] if proj.slides else None

            elif op == "9":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                else:
                    c = input("  Texto   : ").strip()
                    f = input("  Fonte   (Enter=Arial): ").strip() or "Arial"
                    t = input("  Tamanho (Enter=16)  : ").strip()
                    slide.adicionar_elemento(Texto(c, f, int(t) if t.isdigit() else 16))

            elif op == "10":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                else:
                    n = input("  Arquivo: ").strip()
                    l = input("  Largura (Enter=200): ").strip()
                    a = input("  Altura  (Enter=150): ").strip()
                    slide.adicionar_elemento(
                        Imagem(n, int(l) if l.isdigit() else 200,
                                  int(a) if a.isdigit() else 150))

            elif op == "11":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                elif not slide.elementos:
                    print("  x Slide vazio.")
                else:
                    slide.renderizar()
                    c = input("  Buscar (indice ou texto): ").strip()
                    chave = int(c) if c.isdigit() else c
                    achou = None
                    if isinstance(chave, int):
                        if 0 <= chave < len(slide.elementos):
                            achou = slide.elementos[chave]
                    else:
                        for el in slide.elementos:
                            ref = el.conteudo if isinstance(el, Texto) else el.nome
                            if chave.lower() in ref.lower():
                                achou = el; break
                    if achou:
                        print(f"  -> {achou.info()}")
                        print(achou.renderizar())
                    else:
                        print(f"  x '{c}' nao encontrado.")

            elif op == "12":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                elif not slide.elementos:
                    print("  x Slide vazio.")
                else:
                    slide.renderizar()
                    idx = input("  Indice : ").strip()
                    l   = input("  Largura: ").strip()
                    a   = input("  Altura : ").strip()
                    if idx.isdigit() and l.isdigit() and a.isdigit():
                        slide.elementos[int(idx)].alterar_proporcoes(int(l), int(a))

            elif op == "13":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                elif not slide.elementos:
                    print("  x Slide vazio.")
                else:
                    slide.renderizar()
                    idx = input("  Indice: ").strip()
                    if idx.isdigit():
                        slide.remover_elemento(int(idx))

            elif op == "14":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                else:
                    slide.renderizar()

            elif op == "15":
                if not slide:
                    print("  x Selecione um slide primeiro.")
                elif not slide.elementos:
                    print("  x Slide vazio.")
                else:
                    n = input("  Nome do template: ").strip()
                    if n:
                        t = slide.salvar_como_template(n, u)
                        u.templates.append(t)

            elif op == "16":
                todos = list({id(t): t for t in u.templates + biblioteca}.values())
                if not todos:
                    print("  x Sem templates disponiveis.")
                elif not slide:
                    print("  x Selecione um slide primeiro.")
                else:
                    for i, t in enumerate(todos):
                        print(f"  [{i}] {t.nome} [{t.estado}]")
                    idx = input("  Numero: ").strip()
                    if idx.isdigit() and int(idx) < len(todos):
                        slide.aplicar_template(todos[int(idx)])

            elif op == "17":
                if not u.templates:
                    print("  Sem templates.")
                else:
                    for t in u.templates:
                        t.info()

            elif op == "18":
                if not u.templates:
                    print("  x Sem templates.")
                else:
                    for i, t in enumerate(u.templates):
                        print(f"  [{i}] {t.nome} [{t.estado}]")
                    idx = input("  Numero: ").strip()
                    if idx.isdigit() and int(idx) < len(u.templates):
                        publicar_na_biblioteca(u.templates[int(idx)])

            elif op == "19":
                listar_biblioteca()

        input("\n  [Enter para continuar]")


if __name__ == "__main__":
    run()
