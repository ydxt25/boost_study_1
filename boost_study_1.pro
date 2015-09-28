TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += main.cpp

CONFIG +=c++11
LIBS +=-lboost_system -lboost_filesystem -lboost_regex -lboost_date_time -lboost_program_options
