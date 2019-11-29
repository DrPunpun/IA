from collections import Counter


# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2018
# v1.81 - 2018/11/18
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclass AssocOne
class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,float(e2))

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=[]):
        self.declarations = ldecl
    def __str__(self):
        return my_list2string(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    
    ## Set of names of association
    def list_associations(self):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))

    def list_instance_type(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))

    def list_names(self):
        return list(set([d.user for d in self.declarations]))

    def list_types(self):
        return list(set([d.relation.entity2 for d in self.declarations if isinstance(d.relation, Member)] + \
                        [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)] + \
                        [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype)]))

    def list_ent_assoc(self, entity):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) and (d.relation.entity1==entity or d.relation.entity2==entity)]))

    def list_ent_relation(self, entity):
        return list(set([d.relation.name for d in self.declarations if (d.user == entity)]))

    def list_num_assoc(self, user):
        return len(set([d.relation.name for d in self.declarations if d.user == user]))
    
    def list_tup_assoc(self, entity):
        return list(set([(d.user, d.relation.name) for d in self.declarations if (d.relation.entity1==entity or d.relation.entity2==entity)]))

    def check_predec(self, e1, e2):
        dp = [d.relation for d in self.declarations if d.relation.entity1 == e2 and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        if [r for r in dp if r.entity2 == e1] != []:
            return True
        
        return any([self.check_predec(e1, r.entity2) for r in dp])
    
    def predecessor_path(self, e1, e2):
        dp = [d.relation.entity2 for d in self.declarations if d.relation.entity1 == e2 and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        
        if e1 in dp:
            return [e1, e2]
        for p in dp:
            pp = self.predecessor_path(e1, p)
            if pp:
                return pp+  [e2]
        return None
    
    def query(self, entity, assoc=None):
        ancestors = [self.query(d.relation.entity2, assoc) for d in self.declarations if d.relation.entity1 == entity and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        
        return [item for sublist in ancestors for item in sublist] + self.query_local(e1=entity, rel=assoc)
    def query2(self, entity, relation=None):
        ancestors = [self.query2(d.relation.entity2, relation) for d in self.declarations if d.relation.entity1 == entity and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]

        return [item for sublist in ancestors for item in sublist if isinstance(item.relation, Association)] + self.query_local(e1=entity, rel=relation)
    
    def query_cancel(self, entity, assoc):
        ancestors = [self.query_cancel(d.relation.entity2, assoc) for d in self.declarations if d.relation.entity1 == entity and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        
        local_decl = self.query_local(e1 = entity, rel = assoc)
        local_rels = [d.relation.name for d in local_decl]

        return [item for sublist in ancestors for item in sublist if item.relation.name not in local_rels] + local_decl
    def query_down(self, entity, assoc, skip_1st=True):
        descendents = [self.query_down(d.relation.entity1, assoc, False) for d in self.declarations if d.relation.entity2 == entity and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]

        if skip_1st:
            return [item for sublist in descendents for item in sublist]

        return [item for sublist in descendents for item in sublist] + self.query_local(e1=entity, rel=assoc)
        
    def query_induce(self, type, assoc):
        suc = self.query_down(type, assoc)
        
        counter = Counter([s.relation.entity2 for s in suc])
        for v,c in counter.most_common(1):
            return v
    
    def query_local_assoc(self, entity, relation):
        local_decl = self.query_local(e1=entity, rel=relation)
        
        if len(local_decl) > 0 and isinstance(local_decl[0].relation, AssocNum):
            return sum([l.relation.entity2 for l in local_decl])/len(local_decl)
        elif len(local_decl) > 0 and isinstance(local_decl[0].relation, AssocOne):
            c = Counter([l.relation.entity2 for l in local_decl])
            v, count = c.most_common(1)[0]
            return v, count/len(local_decl)
        elif len(local_decl) > 0 and isinstance(local_decl[0].relation, Association):
            c = Counter([l.relation.entity2 for l in local_decl])
            accum = 0
            li = []
            for v,count in c.most_common():
                if accum > 0.75:
                    return li
                li.append((v, count/len(local_decl)))
                accum += count/len(local_decl)

# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    

