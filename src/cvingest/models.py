from calendar import monthrange
from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Span(BaseModel):
    date_range: tuple[datetime, datetime] = Field(
        default_factory=lambda: (datetime.now(), datetime.now())
    )

    @model_validator(mode="before")
    @classmethod
    def parse_span(cls, value):
        if isinstance(value, str):
            start, end = [part.strip() for part in value.split("-", 1)]

            # YYYY - YYYY
            if start.isdigit() and end.isdigit():
                return {
                    "date_range": (
                        datetime(int(start), 1, 1),
                        datetime(int(end), 12, 31),
                    )
                }

            # MM/YYYY - MM/YYYY
            start_month, start_year = map(int, start.split("/"))
            end_month, end_year = map(int, end.split("/"))

            end_day = monthrange(end_year, end_month)[1]

            return {
                "date_range": (
                    datetime(start_year, start_month, 1),
                    datetime(end_year, end_month, end_day),
                )
            }

        return value

    def as_tuple(self) -> tuple[str, str]:
        start, end = self.date_range

        # Detect year-only ranges based on the normalized dates
        is_year_only = (
            start.month == 1 and start.day == 1 and end.month == 12 and end.day == 31
        )

        if is_year_only:
            return (
                start.strftime("%Y"),
                end.strftime("%Y"),
            )

        return (
            start.strftime("%m/%Y"),
            end.strftime("%m/%Y"),
        )


class ExperienceItem(BaseModel):
    company: str
    domain: str | None = Field(default=None)
    span: Span = Field(default_factory=Span)
    role: str
    team: str | None = Field(default=None)
    division: str | None = Field(default=None)
    description: str | None = Field(default=None)
    keywords: set[str] | None = Field(default_factory=set)


class EducationItem(BaseModel):
    school: str
    span: Span = Field(default_factory=Span)
    program: str | None = Field(default=None)
    major: str | None = Field(default=None)
    minor: str | None = Field(default=None)
    description: str | None = Field(default=None)
    keywords: set[str] = Field(default_factory=set)


class SkillItem(BaseModel):
    name: str
    alias: set[str] = Field(default_factory=set)
    description: str | None = Field(default=None)


class LanguageItem(BaseModel):
    name: str
    level: str


class Personal(BaseModel):
    name: str
    email: str
    phone: str
    linkedin: str
    city: str
    country: str
    github: str


class MasterCV(BaseModel):
    personal: Personal | None
    languages: list[LanguageItem] = Field(default_factory=list)
    skills: list[SkillItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    experience: list[ExperienceItem] = Field(default_factory=list)


class Education(BaseModel):
    school: str = Field(default="...")
    degree: str | None = Field(default="...")
    program: str | None = Field(default="...")
    major: str | None = Field(default="...")
    span: Span | None = Field(default_factory=Span)
    description: str | None = Field(default="...")


class Experience(BaseModel):
    company: str = Field(default="...")
    title: str = Field(default="...")
    span: Span = Field(default_factory=Span)
    description: str = Field(default="...")


class TailoredCV(BaseModel):
    personal: Personal | None = Field(default=None)
    education: list[Education]
    experience: list[Experience]
    skills: list[str]
