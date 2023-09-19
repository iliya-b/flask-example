import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, FilesInfo as FilesInfoModel


class FilesInfo(SQLAlchemyObjectType):
    class Meta:
        model = FilesInfoModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    dataset_info = graphene.Field(FilesInfo, fileID=graphene.String())

    all_files = SQLAlchemyConnectionField(FilesInfo.connection)

    def resolve_dataset_info(self, info, fileID):
        return FilesInfo.get_query(info).filter(FilesInfoModel.fileID == fileID).first()


schema = graphene.Schema(query=Query)
