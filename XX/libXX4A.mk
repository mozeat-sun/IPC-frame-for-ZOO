include ../Makefile_tpl_cov
TARGET   := libXX4A.so
SRCEXTS  := .cpp
INCDIRS  := ./inc ./com
SOURCES  := ./lib/XX4A.cpp ./lib/XX4I.cpp
SRCDIRS  :=
CFLAGS   :=
CXXFLAGS := -std=c++11
CPPFLAGS := $(GCOV_FLAGS)  -fPIC
LDFLAGS  := $(GCOV_LINK)  -lnsl -shared

include ../Project_config
include ../Makefile_tpl_zoo