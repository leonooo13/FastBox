from sqlmodel import SQLModel, Field
from datetime import date
from enum import Enum


# 定义项目状态的枚举类
class ProjectStatus(str, Enum):
    pending = "pending"  # 待定
    in_progress = "in_progress"  # 进行中
    completed = "completed"  # 已完成


# 项目模型
class Project(SQLModel, table=True):
    id: int = Field(primary_key=True)  # 项目ID，主键
    name: str = Field(max_length=100)  # 项目名称
    description: str = Field(max_length=500)  # 项目描述
    deadline: date = Field(default=None)  # 截止日期
    status: ProjectStatus = Field(default=ProjectStatus.pending)  # 项目状态，默认待定
    created_at: date = Field(default_factory=date.today)  # 项目创建日期，默认当前日期
    updated_at: date = Field(default_factory=date.today)  # 项目更新时间，默认当前日期

    # 可选的字段，可以根据需求扩展
    file: str = Field(default=None, nullable=True)  # 上传的文件路径（可选）
    owner_id: int = Field(default=None, nullable=True)  # 项目负责人ID（可选）

    class Config:
        use_enum_values = True  # 自动将枚举转换为字符串表示
