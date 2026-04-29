from typing import Optional
from modelos import Projeto, Template


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
        self.amigos:    list['Usuario'] = []
        self.pendentes: list['Usuario'] = []

    def login(self, senha: str) -> bool:
        if self.senha == senha:
            self.status = "Logado"
            print(f"  + {self.email} logado.")
            return True
        print("  x Senha incorreta.")
        return False

    def logout(self):
        self.status = "Deslogado"
        print(f"  {self.email} deslogado.")

    def enviar_solicitacao(self, outro: 'Usuario'):
        if outro is self:
            print("  x Voce nao pode se adicionar.")
        elif outro in self.amigos:
            print(f"  x {outro.email} ja e seu amigo.")
        elif self in outro.pendentes:
            print(f"  x Solicitacao ja enviada para {outro.email}.")
        else:
            outro.pendentes.append(self)
            print(f"  + Solicitacao enviada para {outro.email}.")

    def aceitar_solicitacao(self, solicitante: 'Usuario'):
        if solicitante in self.pendentes:
            self.pendentes.remove(solicitante)
            self.amigos.append(solicitante)
            solicitante.amigos.append(self)
            print(f"  + Agora voce e {solicitante.email} sao amigos!")
        else:
            print(f"  x Nenhuma solicitacao de {solicitante.email}.")

    def recusar_solicitacao(self, solicitante: 'Usuario'):
        if solicitante in self.pendentes:
            self.pendentes.remove(solicitante)
            print(f"  + Solicitacao de {solicitante.email} recusada.")
        else:
            print(f"  x Nenhuma solicitacao de {solicitante.email}.")

    def remover_amigo(self, outro: 'Usuario'):
        if outro in self.amigos:
            self.amigos.remove(outro)
            if self in outro.amigos:
                outro.amigos.remove(self)
            print(f"  + {outro.email} removido dos amigos.")
        else:
            print(f"  x {outro.email} nao e seu amigo.")

    def atualizar_perfil(self, bio: Optional[str], foto: Optional[str],
                         restrito: Optional[bool]):
        if bio      is not None: self.biografia     = bio;     print("  + Biografia atualizada.")
        if foto     is not None: self.foto_perfil   = foto;    print(f"  + Foto: '{foto}'")
        if restrito is not None: self.modo_restrito = restrito; print(f"  + Modo restrito: {'on' if restrito else 'off'}")

    def criar_projeto(self, nome: str) -> Projeto:
        p = Projeto(nome, self)
        self.projetos.append(p)
        print(f"  + Projeto '{nome}' criado!")
        return p

    def info(self):
        print("  " + "-" * 52)
        print(f"  Email    : {self.email} [{self.status}]")
        print(f"  Biografia: {self.biografia or '(vazia)'}")
        print(f"  Foto     : {self.foto_perfil or '(nenhuma)'}")
        print(f"  Restrito : {'Sim' if self.modo_restrito else 'Nao'}")
        print(f"  Projetos : {len(self.projetos)}")
        print(f"  Templates: {len(self.templates)}")
        print(f"  Amigos   : {len(self.amigos)}")
        if self.pendentes:
            print(f"  * {len(self.pendentes)} solicitacao(oes) pendente(s)!")


biblioteca: list[Template] = []

def publicar_na_biblioteca(t: Template):
    t.publicar()
    if t not in biblioteca:
        biblioteca.append(t)

def listar_biblioteca():
    if not biblioteca:
        print("  (biblioteca vazia)")
    else:
        for i, t in enumerate(biblioteca):
            print(f"  [{i}] {t.nome} -- {t.criador.email} ({len(t.elementos)} elem.)")
