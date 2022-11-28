# Cloud Project
 
## O que foi realizado no projeto (conceito C+):
* Desenvolvimento de uma aplicação capaz de provisionar uma infraestrutura por meio de uma interface amigável.
* Possibilidade de criar:  VPC; sub-rede; múltiplas instâncias com tipos de configuração de hosts diferentes; security group e suas regras; usuário no IAM.
* Possibilidade de deletar: instâncias; grupos de segurança; usuário.
* Método GET que lista todas instâncias e suas regiões, usuários, grupos de segurança e suas regras
 
## Pré-requisitos
O projeto foi desenvolvido em alguns pilares, os quais serão necessários para seu funcionamento apropriado, sendo eles:
* Terraform > https://developer.hashicorp.com/terraform/downloads
* AWS > https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
* FastAPI > https://fastapi.tiangolo.com/tutorial/#install-fastapi
 
## Por onde começar
Em poucas palavras, terraform é uma ferramenta de IaC open source, que permite ao usuário criar e gerenciar uma cloud por meio de uma linguagem declarativa. Com isso, torna-se mais fácil construir uma estrutura em código, podendo escalonar ou destruir a nuvem de forma simples.
 
#### O que é?
Para um melhor entendimendo leia os seguintes textos https://developer.hashicorp.com/terraform/intro e https://medium.com/devops-mojo/terraform-overview-introduction-to-terraform-what-is-terraform-843bf65b83fb
 
#### Como funciona uma linguagem declarativa?
Uma linguagem declarativa demanda que você escreva exatamente o que precisa, então, por debaixo dos panos o operacional acontece, trazendo ao usuário o requerido.
 
Vamos supor, por exemplo, que vamos subir uma instância na AWS manualmente. Para isso, precisaríamos entrar no dashboard, na área EC2, por exemplo, e atribuirmos uma imagem e um tipo à instância. Na linguagem declarativa, o funcionamento é o mesmo, para um determinado recurso, atribuímos todas as informações realmente necessárias para sua criação, fora outros adicionais, caso o projeto demande. Um código em Terraform para operacionalizar nossa instância, tem a seguinte forma:
 
```
resource "aws_instance" "web" {
 ami           = "${data.aws_ami.ubuntu.id}"
 instance_type = "t2.micro"
 
 tags = {
   Name = "HelloWorld"
 }
}
```
 
Para a AWS, poderíamos construir diversos blocos de recursos diferentes, vale a leitura rápida das diversas possibilidades, https://registry.terraform.io/providers/hashicorp/aws/2.34.0/docs. Além disso, poderíamos realizar o mesmo projeto para diferentes provedores de nuvem, adaptando apenas a estrutura de blocos requerida por cada provedor.
 
Por mais que a linguagem pareça simples, podemos estruturar o projeto de diversas maneiras. A maneira mais simples, pode ser realizada com um estudo básico da documentação ou de vídeos introdutórios como o seguinte curso https://www.youtube.com/playlist?list=PLWQmZVQayUUIgSmOj3GPH2BJcn0hOzIaP (basta assistir até a aula 14).
 
Para realizar um projeto um pouco mais robusto, podemos sempre avançar na frente das boas práticas https://cloud.google.com/docs/terraform/best-practices-for-terraform?hl=pt-br. Outra forma é estruturar o projeto em módulos de terraform, o que é apresentado no decorrer do curso que acabo de citar.
 
 
#### Como FastAPI se relaciona?
Na realidade, há pouquíssimo conteúdo que une Terraform a FastAPI disponível na internet. Optei por utilizar a ferramenta, pois podemos acessar o localhost:8000/docs, por exemplo, e testar de maneira muito simples todas as endpoits criadas. O fato de criar cada uma das chamadas por vez, facilita o entendimento de como cada bloco opera no contexto da cloud que estamos construindo. Além da ótima usabilidade, acredito que a ferramenta permite modificar e aumentar o escopo do projeto de forma rápida e simples.
 
 
## Como rodar?
 
Com todas as dependências instaladas, pasta rodar o comando:
``` uvicorn api.main:app```
 
Acesse a url http://127.0.0.1:8000/docs, para encontrar a interface amigável da FastAPI. Assim, é possível os métodos mais básicos, para adicionar usuários IAM, instancias e regras de segurança ao seu projeto. Quando adicionar ou remover o desejado, basta ir para a tag de Terraform e realizar um post com a chamada **apply** para dar início ou realizar alterações na sua cloud. A mesma chamada, também funciona para destruir tudo, sendo necessário realizar a chamada com **destroy**
 
 
## Próximas iterações
* Por mais que o projeto tenha sido feito em módulos, pouquíssimos recursos podem ser alterados de forma rápida. Seria interessante facilitar a criação de **Instância em mais de uma região; Associar algum tipo de restrição de acesso a um usuário**
* A API foi desenvolvida sem testes e com poucas chamadas para erros HTTP, é interessante impedir a criação de recursos inexistentes ou de atribuir uma variável errada a um recurso. Há uma grande possibilidade de erros, em se tratando da criação de recursos na AWS, portanto é necessário melhorar a estrutura de prevenção quanto a isso
* O método GET, que permite ao usuário visualizar o estado da nuvem, é baseado em percorrer o arquivo tfstate e buscar as informações relevantes. O correto seria utilizar outputs ou data source (https://developer.hashicorp.com/terraform/language/data-sources) para apresentar ao usuário somente o necessário
* Para atingir o conceito A, na matéria, seria necessário criar um HA de servidores web.

