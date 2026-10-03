import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const out = fileURLToPath(new URL('../', import.meta.url));
const wb = Workbook.create();
function sheet(name, widths, title) {
  const s = wb.worksheets.add(name); s.showGridLines = false;
  s.getRange('A1:F40').format.font = {name:'Arial',size:11,color:'#243247'};
  widths.forEach((w,i)=>s.getRangeByIndexes(0,i,40,1).format.columnWidth=w);
  s.getRange('A2').values=[[title]]; s.getRange('A2').format.font={name:'Arial',size:16,bold:true};
  return s;
}
function table(s,row,data,name) {
  const r=s.getRangeByIndexes(row-1,0,data.length,data[0].length); r.values=data;
  r.format.rowHeight=36; r.format.wrapText=true; r.format.verticalAlignment='center';
  s.tables.add(r.address ?? `A${row}:${String.fromCharCode(64+data[0].length)}${row+data.length-1}`,true,name);
  const h=s.getRangeByIndexes(row-1,0,1,data[0].length);
  h.format.fill='#263F64'; h.format.font={name:'Arial',size:11,bold:true,color:'#FFFFFF'};
  h.format.horizontalAlignment='center';
}
const s=sheet('Estrutura',[16,19,22,18,34,49],'Estrutura proposta do banco');
s.getRange('A4').values=[['Banco: posts_app. MySQL com tabelas InnoDB e conjunto de caracteres utf8mb4.']];
table(s,6,[['Tabela','Coluna','Tipo MySQL','Obrigatório','Regra / padrão','Finalidade'],
['usuarios','id','INT','Sim','PRIMARY KEY; AUTO_INCREMENT','Identificador gerado pelo banco.'],
['usuarios','nome','VARCHAR(100)','Sim','NOT NULL','Nome exibido no perfil.'],
['usuarios','username','VARCHAR(50)','Sim','NOT NULL; UNIQUE','Nome único usado para identificar o perfil.'],
['usuarios','bio','VARCHAR(255)','Não','NULL permitido','Descrição curta do usuário.'],
['posts','id','INT','Sim','PRIMARY KEY; AUTO_INCREMENT','Identificador gerado pelo banco.'],
['posts','usuario_id','INT','Sim','NOT NULL; FOREIGN KEY','Referencia usuarios.id; deve existir um autor.'],
['posts','conteudo','VARCHAR(280)','Sim','NOT NULL','Texto do post, até 280 caracteres.'],
['posts','criado_em','DATETIME','Sim','DEFAULT CURRENT_TIMESTAMP; NOT NULL','Data e hora de criação preenchidas pelo banco.']], 'Campos');
s.getRange('A17').values=[['Relação: um usuário pode ter vários posts; cada post pertence a um usuário.']];
s.getRange('A19').values=[['Origem: proposta discutida no projeto. Os exemplos da próxima aba são fictícios.']];
const d=sheet('Dados de exemplo',[23,55,46],'Carga inicial sugerida');
table(d,4,[['username','nome','bio'],['ana','Ana Silva','Aprendendo desenvolvimento web'],['bruno','Bruno Souza','Estudante de tecnologia']], 'UsuariosExemplo');
d.getRange('A8').values=[['Posts: procurar o ID pelo username do autor antes de inserir em usuario_id.']];
const texts=['Hoje comecei a aprender Flask!','Minha primeira rota com Flask funcionou.','Aprendendo JSON com Flask.','Conectando Flask ao MySQL.','Organizando Controllers no Flask.','Criando Models para o projeto Flask.','Testando a busca de posts com Flask.','Aprendendo paginação com Flask.','Preparando templates no Flask.','Montando o perfil de usuário com Flask.','Tratando erros na API Flask.','Finalizando meu projeto Flask.'];
table(d,10,[['Autor (username)','conteudo','Preenchimento automático'],...texts.map((t,i)=>[i%2?'bruno':'ana',t,'id e criado_em: gerados pelo MySQL'])], 'PostsExemplo');
d.getRange('A25').values=[['Teste: buscar Flask deve encontrar 12 posts (10 na página 1 e 2 na página 2).']];
d.getRange('A27').values=[['IDs não são fixos: utilize os IDs reais dos usuários criados na máquina de destino.']];
const e=sheet('Entregas',[25,61,65],'O que combinar com o colega');
table(e,4,[['Entrega sugerida','Para que serve','Como será usada no seu computador'],
['schema.sql','Arquivo de texto com comandos SQL para criar posts_app, usuarios e posts.','Executar no MySQL local antes da carga inicial. Não é o banco em si.'],
['seed.py','Programa Python que conecta ao MySQL e usa cursor para inserir os dados iniciais.','Executar manualmente após criar as tabelas. Deve evitar duplicações se repetido.'],
['Instruções de execução','Versão do MySQL testada, biblioteca Python necessária e ordem dos comandos.','Instalar os requisitos e configurar host, porta, usuário e senha locais.'],
['Controle de repetição','Definir no seed.py como reconhecer a carga já realizada, incluindo os posts.','Verificar que uma segunda execução não duplica registros nem apaga dados existentes.']], 'Entregas');
e.getRange('A5:C8').format.rowHeight=68;
e.getRange('A11').values=[['Sequência: instalar MySQL → executar schema.sql → executar seed.py → iniciar Flask.']];
e.getRange('A13').values=[['SQL é a linguagem entendida pelo banco. O cursor Python envia comandos SQL ao MySQL.']];
e.getRange('A15').values=[['Um arquivo .sql também pode inserir dados; nesta proposta, essas inserções ficam no seed.py.']];
e.getRange('A17').values=[['Executar o seed manualmente; não disparar a carga ao iniciar Flask nem ao acessar uma rota.']];
e.getRange('A19').values=[['Cada computador terá seu próprio banco. Os scripts reproduzem a estrutura e os dados iniciais.']];
e.getRange('A21').values=[['Esta planilha é uma especificação: não cria o banco e não contém os scripts prontos.']];
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Estrutura!A6:F14',include:'values',tableMaxRows:9,tableMaxCols:6,maxChars:2500})).ndjson);
for(const [n,r] of [['Estrutura','A1:F20'],['Dados de exemplo','A1:C28'],['Entregas','A1:C22']]) {
 const b=await wb.render({sheetName:n,range:r,scale:1,format:'png'});
 await fs.writeFile(`${out}/${n}.png`,new Uint8Array(await b.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(`${out}/planejamento_banco_posts.xlsx`);
console.log('Exportado planejamento_banco_posts.xlsx');
