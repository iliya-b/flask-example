from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/postgres', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Device(Base):
    __tablename__ = 'Devices'

    deviceID = Column(String(255), primary_key=True, index=True)
    userAgent = Column(String(255))
    browser = Column(String(255))
    engine = Column(String(255))
    os = Column(String(255))
    osVersion = Column(String(255))
    device = Column(String(255))
    cpu = Column(String(255))
    screen = Column(String(255))
    plugins = Column(String(255))
    timeZone = Column(String(255))
    language = Column(String(255))
    createdAt = Column(DateTime(True), nullable=False)


class Permission(Base):
    __tablename__ = 'Permissions'

    id = Column(Integer, primary_key=True)
    permission = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = 'Users'

    userID = Column(UUID, primary_key=True)
    fullName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    companyOrAffiliation = Column(String(255), nullable=False)
    occupation = Column(String(255), nullable=False)
    pwdHash = Column(String(255), nullable=False)
    accountStatus = Column(String(255), nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class Code(Base):
    __tablename__ = 'Codes'

    codeID = Column(UUID, primary_key=True)
    type = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)
    expiringDate = Column(DateTime(True), nullable=False)
    userID = Column(ForeignKey(
        'Users.userID', onupdate='CASCADE'), nullable=False)
    deviceID = Column(ForeignKey('Devices.deviceID',
                      ondelete='SET NULL', onupdate='CASCADE'))

    Device = relationship('Device')
    User = relationship('User')


class Feedback(Base):
    __tablename__ = 'Feedbacks'

    feedbackID = Column(UUID, primary_key=True)
    userID = Column(ForeignKey(
        'Users.userID', ondelete='SET NULL', onupdate='CASCADE'))
    rating = Column(Integer, nullable=False)
    subject = Column(String(255))
    text = Column(Text, nullable=False)
    createdAt = Column(DateTime(True), nullable=False)

    User = relationship('User')


class FilesInfo(Base):
    __tablename__ = 'FilesInfo'

    fileID = Column(UUID, primary_key=True)
    createdAt = Column(DateTime(True), nullable=False,
                       server_default=text("now()"))
    userID = Column(ForeignKey(
        'Users.userID', ondelete='SET NULL', onupdate='CASCADE'))
    isBuiltIn = Column(Boolean, nullable=False, server_default=text("false"))
    isValid = Column(Boolean, nullable=False, server_default=text("true"))
    mimeType = Column(String(255))
    encoding = Column(String(255))
    fileName = Column(Text)
    originalFileName = Column(Text, nullable=False)
    hasHeader = Column(Boolean, nullable=False)
    delimiter = Column(String(255), nullable=False)
    renamedHeader = Column(Text)
    rowsCount = Column(Integer)
    countOfColumns = Column(Integer)
    path = Column(String(255), unique=True)
    deletedAt = Column(DateTime(True))

    User = relationship('User')


class FilesFormat(FilesInfo):
    __tablename__ = 'FilesFormat'

    fileID = Column(ForeignKey('FilesInfo.fileID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    inputFormat = Column(String(255), nullable=False)
    tidColumnIndex = Column(Integer)
    itemColumnIndex = Column(Integer)
    hasTid = Column(Boolean)
    deletedAt = Column(DateTime(True))


class Role(Base):
    __tablename__ = 'Roles'

    roleID = Column(UUID, primary_key=True)
    userID = Column(ForeignKey('Users.userID', ondelete='CASCADE',
                    onupdate='CASCADE'), nullable=False)
    type = Column(String(255), nullable=False)
    permissionIndices = Column(String(255))

    User = relationship('User')


class Session(Base):
    __tablename__ = 'Sessions'

    sessionID = Column(UUID, primary_key=True)
    userID = Column(ForeignKey('Users.userID', ondelete='CASCADE',
                    onupdate='CASCADE'), nullable=False)
    deviceID = Column(ForeignKey('Devices.deviceID',
                      onupdate='CASCADE'), nullable=False)
    status = Column(String(255), nullable=False)
    accessTokenIat = Column(Integer)
    refreshTokenIat = Column(Integer)
    createdAt = Column(DateTime(True), nullable=False)

    Device = relationship('Device')
    User = relationship('User')


class TasksState(Base):
    __tablename__ = 'TasksState'

    taskID = Column(UUID, primary_key=True)
    isPrivate = Column(Boolean, nullable=False, server_default=text("false"))
    attemptNumber = Column(Integer, nullable=False, server_default=text("0"))
    status = Column(String(255), nullable=False)
    phaseName = Column(String(255))
    currentPhase = Column(Integer)
    progress = Column(Float(53), nullable=False,
                      server_default=text("'0'::double precision"))
    maxPhase = Column(Integer)
    errorMsg = Column(Text)
    isExecuted = Column(Boolean, nullable=False, server_default=text("false"))
    elapsedTime = Column(Float(53))
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))
    userID = Column(ForeignKey(
        'Users.userID', ondelete='SET NULL', onupdate='CASCADE'))

    User = relationship('User')


class ARTasksConfig(TasksState):
    __tablename__ = 'ARTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    minSupportAR = Column(Float, nullable=False)
    minConfidence = Column(Float, nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class ARTasksResult(TasksState):
    __tablename__ = 'ARTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    deps = Column(Text)
    depsAmount = Column(Integer)
    valueDictionary = Column(Text)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class CFDTasksConfig(TasksState):
    __tablename__ = 'CFDTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    maxLHS = Column(Integer, nullable=False)
    minSupportCFD = Column(Integer, nullable=False)
    minConfidence = Column(Float, nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class CFDTasksResult(TasksState):
    __tablename__ = 'CFDTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    deps = Column(Text)
    depsAmount = Column(Integer)
    PKColumnIndices = Column(Text)
    withPatterns = Column(Text)
    withoutPatterns = Column(Text)
    valueDictionary = Column(Text)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class FDTasksConfig(TasksState):
    __tablename__ = 'FDTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    errorThreshold = Column(Float, nullable=False)
    maxLHS = Column(Integer, nullable=False)
    threadsCount = Column(Integer, nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class FDTasksResult(TasksState):
    __tablename__ = 'FDTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    deps = Column(Text)
    depsAmount = Column(Integer)
    PKColumnIndices = Column(Text)
    withoutPatterns = Column(Text)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class MFDTasksConfig(TasksState):
    __tablename__ = 'MFDTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    parameter = Column(Float, nullable=False)
    lhsIndices = Column(String(255), nullable=False)
    rhsIndices = Column(String(255), nullable=False)
    distanceToNullIsInfinity = Column(Boolean, nullable=False)
    metric = Column(String(255), nullable=False)
    q = Column(Integer, nullable=False)
    metricAlgorithm = Column(String(255))
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class MFDTasksResult(TasksState):
    __tablename__ = 'MFDTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    deps = Column(Text)
    depsAmount = Column(Integer)
    result = Column(Boolean)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class SpecificTypoClusterTasksConfig(TasksState):
    __tablename__ = 'SpecificTypoClusterTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    parentTaskID = Column(UUID, nullable=False)
    clusterID = Column(Integer, nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class SpecificTypoClusterTasksResult(TasksState):
    __tablename__ = 'SpecificTypoClusterTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    suspiciousIndices = Column(Text)
    squashedNotSortedCluster = Column(Text)
    squashedSortedCluster = Column(Text)
    squashedItemsAmount = Column(Integer)
    notSquashedItemsAmount = Column(Integer)
    notSquashedNotSortedCluster = Column(Text)
    notSquashedSortedCluster = Column(Text)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class StatsTasksConfig(TasksState):
    __tablename__ = 'StatsTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    threadsCount = Column(Integer, nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class StatsTasksResult(TasksState):
    __tablename__ = 'StatsTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class TasksConfig(TasksState):
    __tablename__ = 'TasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    fileID = Column(ForeignKey('FilesInfo.fileID',
                    ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    algorithmName = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))

    FilesInfo = relationship('FilesInfo')


class TypoClusterTasksConfig(TasksState):
    __tablename__ = 'TypoClusterTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    typoFD = Column(String(255), nullable=False)
    parentTaskID = Column(UUID, nullable=False)
    radius = Column(Float(53), nullable=False)
    ratio = Column(Float(53), nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class TypoClusterTasksResult(TasksState):
    __tablename__ = 'TypoClusterTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    TypoClusters = Column(Text)
    suspiciousIndices = Column(Text)
    clustersCount = Column(Text)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class TypoFDTasksConfig(TasksState):
    __tablename__ = 'TypoFDTasksConfig'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    errorThreshold = Column(Float, nullable=False)
    maxLHS = Column(Integer, nullable=False)
    threadsCount = Column(Integer, nullable=False)
    preciseAlgorithm = Column(String(255), nullable=False)
    approximateAlgorithm = Column(String(255), nullable=False)
    metric = Column(String(255), nullable=False)
    defaultRadius = Column(Float(53), nullable=False)
    defaultRatio = Column(Float(53), nullable=False)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class TypoFDTasksResult(TasksState):
    __tablename__ = 'TypoFDTasksResult'

    taskID = Column(ForeignKey('TasksState.taskID',
                    ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    deps = Column(Text)
    depsAmount = Column(Integer)
    PKColumnIndices = Column(Text)
    createdAt = Column(DateTime(True), nullable=False)
    deletedAt = Column(DateTime(True))


class ColumnStat(Base):
    __tablename__ = 'ColumnStats'

    fileID = Column(ForeignKey('FilesInfo.fileID',
                    onupdate='CASCADE'), primary_key=True, nullable=False)
    columnIndex = Column(Integer, primary_key=True, nullable=False)
    type = Column(String(255), nullable=False)
    distinct = Column(Integer)
    isCategorical = Column(Boolean)
    count = Column(Integer)
    avg = Column(String(255))
    STD = Column(String(255))
    skewness = Column(String(255))
    kurtosis = Column(String(255))
    min = Column(String(255))
    max = Column(String(255))
    sum = Column(String(255))
    quantile25 = Column(String(255))
    quantile50 = Column(String(255))
    quantile75 = Column(String(255))
    deletedAt = Column(DateTime(True))

    FilesInfo = relationship('FilesInfo')
