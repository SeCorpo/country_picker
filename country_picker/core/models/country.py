from typing import List, Optional, Dict
from pydantic import BaseModel, Field

""" Derived from json response, using dynamic schema generation """

class Currency(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None

class Language(BaseModel):
    iso639_1: Optional[str] = None
    iso639_2: Optional[str] = None
    name: Optional[str] = None
    nativeName: Optional[str] = None

class RegionalBloc(BaseModel):
    acronym: Optional[str] = None
    name: Optional[str] = None
    otherNames: Optional[List[str]] = Field(default_factory=list)
    otherAcronyms: Optional[List[str]] = Field(default_factory=list)

class Flags(BaseModel):
    svg: Optional[str] = None
    png: Optional[str] = None

class Country(BaseModel):
    name: str
    topLevelDomain: List[str] = Field(default_factory=list)
    alpha2Code: str
    alpha3Code: str
    callingCodes: List[ str] = Field(default_factory=list)
    capital: Optional[str] = ""
    altSpellings: List[str] = Field(default_factory=list)
    subregion: Optional[str] = ""
    region: Optional[str] = ""
    population: Optional[int] = 0
    latlng: List[float] = Field(default_factory=list)
    demonym: Optional[str] = ""
    area: Optional[float] = None
    gini: Optional[float] = None
    timezones: List[str] = Field(default_factory=list)
    borders: List[str] = Field(default_factory=list)
    nativeName: Optional[str] = ""
    numericCode: Optional[str] = ""
    flags: Optional[Flags] = None
    currencies: List[Currency] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    translations: Dict[str, str] = Field(default_factory=dict)
    flag: Optional[str] = None
    regionalBlocs: List[RegionalBloc] = Field(default_factory=list)
    cioc: Optional[str] = None
    independent: Optional[bool] = None

    model_config = {'extra': 'allow'}