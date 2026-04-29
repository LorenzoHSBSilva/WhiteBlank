from elementos import ElementoGrafico, Texto, Imagem


class Template:
    def __init__(self, nome: str, elementos: list, criador):
        self.nome      = nome
        self.elementos = elementos
        self.criador   = criador
        self.estado    = "privado"

    def publicar(self):
        self.estado = "publicado"
        print(f"  + Template '{self.nome}' publicado na biblioteca!")

    def info(self):
        print(f"  {self.nome} [{self.estado}] -- {self.criador.email} -- {len(self.elementos)} elem.")


class Slide:
    def __init__(self, ordem: int):
        self.ordem     = ordem
        self.elementos: list[ElementoGrafico] = []

    def adicionar_elemento(self, el: ElementoGrafico):
        self.elementos.append(el)
        label = el.conteudo[:25] if isinstance(el, Texto) else el.nome
        print(f"  + {'Texto' if isinstance(el, Texto) else 'Imagem'} '{label}' adicionado ao Slide {self.ordem}")

    def remover_elemento(self, idx: int):
        if 0 <= idx < len(self.elementos):
            print(f"  - Removido: {self.elementos.pop(idx).info()}")
        else:
            print("  x Indice invalido.")

    def salvar_como_template(self, nome: str, criador) -> Template:
        dados = []
        for el in self.elementos:
            if isinstance(el, Texto):
                dados.append({"tipo": "texto", "conteudo": el.conteudo, "fonte": el.fonte,
                               "tamanho": el.tamanho, "cor": el.cor,
                               "largura": el.largura, "altura": el.altura})
            else:
                dados.append({"tipo": "imagem", "nome": el.nome,
                               "largura": el.largura, "altura": el.altura})
        t = Template(nome, dados, criador)
        print(f"  + Template '{nome}' criado com {len(dados)} elem.")
        return t

    def aplicar_template(self, t: Template):
        for d in t.elementos:
            el = (Texto(d["conteudo"], d.get("fonte", "Arial"), d.get("tamanho", 16),
                        d.get("cor", "preto"), d.get("largura", 200), d.get("altura", 50))
                  if d["tipo"] == "texto"
                  else Imagem(d["nome"], d.get("largura", 200), d.get("altura", 150)))
            self.adicionar_elemento(el)
        print(f"  + Template '{t.nome}' aplicado.")

    def renderizar(self):
        print("  " + "-" * 52)
        print(f"  SLIDE {self.ordem}  --  {len(self.elementos)} elemento(s)")
        print("  " + "-" * 52)
        if not self.elementos:
            print("  (vazio)")
            return
        for i, el in enumerate(self.elementos):
            print(f"\n  [{i}] {el.info()}")
            print(el.renderizar())


class Projeto:
    def __init__(self, nome: str, dono):
        self.nome    = nome
        self.dono    = dono
        self.slides: list[Slide] = [Slide(1)]
        self.membros: list       = [dono]

    def adicionar_slide(self) -> Slide:
        s = Slide(len(self.slides) + 1)
        self.slides.append(s)
        print(f"  + Slide {s.ordem} adicionado.")
        return s

    def remover_slide(self, idx: int):
        if len(self.slides) <= 1:
            print("  x Projeto precisa ter ao menos 1 slide.")
        elif 0 <= idx < len(self.slides):
            s = self.slides.pop(idx)
            for i, sl in enumerate(self.slides): sl.ordem = i + 1
            print(f"  - Slide {s.ordem} removido.")
        else:
            print("  x Indice invalido.")

    def adicionar_membro(self, u):
        if u in self.membros:
            print(f"  x {u.email} ja e membro.")
        else:
            self.membros.append(u)
            print(f"  + {u.email} adicionado ao projeto.")

    def remover_membro(self, u):
        if u is self.dono:
            print("  x O dono nao pode ser removido.")
        elif u in self.membros:
            self.membros.remove(u)
            print(f"  - {u.email} removido.")
        else:
            print(f"  x {u.email} nao e membro.")

    def info(self):
        print("  " + "-" * 52)
        print(f"  Projeto : {self.nome}")
        print(f"  Dono    : {self.dono.email}")
        print(f"  Slides  : {len(self.slides)}")
        print(f"  Membros : {', '.join(m.email for m in self.membros)}")
