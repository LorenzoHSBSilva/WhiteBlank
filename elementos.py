from abc import ABC, abstractmethod


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
                 tamanho: int = 16, cor: str = "preto",
                 largura: int = 200, altura: int = 50):
        super().__init__(largura, altura)
        self.conteudo = conteudo
        self.fonte    = fonte
        self.tamanho  = tamanho
        self.cor      = cor

    def alterar_proporcoes(self, nova_largura: int, nova_altura: int):
        escala = nova_altura / self.altura if self.altura else 1
        self.tamanho = max(8, int(self.tamanho * escala))
        self.largura, self.altura = nova_largura, nova_altura
        print(f"  + Texto redimensionado -> {nova_largura}x{nova_altura}, fonte: {self.tamanho}pt")

    def renderizar(self) -> str:
        b = "-" * (len(self.conteudo) + 4)
        return (f"  +{b}+\n"
                f"  |  {self.conteudo}  |  [{self.fonte}, {self.tamanho}pt, {self.cor}]\n"
                f"  +{b}+")


class Imagem(ElementoGrafico):
    def __init__(self, nome: str, largura: int = 200, altura: int = 150):
        super().__init__(largura, altura)
        self.nome      = nome
        self.proporcao = largura / altura if altura else 1

    def alterar_proporcoes(self, nova_largura: int, nova_altura: int):
        nova_prop = nova_largura / nova_altura if nova_altura else 1
        aviso = (f" ! distorcao ({self.proporcao:.2f}->{nova_prop:.2f})"
                 if abs(nova_prop - self.proporcao) > 0.1 else "")
        self.largura, self.altura = nova_largura, nova_altura
        print(f"  + Imagem redimensionada -> {nova_largura}x{nova_altura}{aviso}")

    def renderizar(self) -> str:
        w = max(20, min(self.largura // 10, 36))
        return (f"  +{'='*w}+\n"
                f"  | {'[IMG] ' + self.nome:^{w-1}}|\n"
                f"  | {f'{self.largura}x{self.altura}px':^{w-1}}|\n"
                f"  +{'='*w}+")
