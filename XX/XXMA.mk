include ../Makefile_tpl_cov

TARGET   := XXMA
SRCEXTS  := .c
INCDIRS  := ./inc ./com
SOURCES  := 
SRCDIRS  := ./bin ./lib
CFLAGS   := 
CXXFLAGS := -std=c++11
CPPFLAGS := 
LDFPATH  := 
LDFLAGS  := $(GCOV_LINK) $(LDFPATH) -lTR4A -lEH4A -lMM4A -lMQ4A -lCOMMON

include ../Project_config
include ../Makefile_tpl_zoo