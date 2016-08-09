BUILT_SOURCES = $(srcdir)/pire_wrap.cpp
CYTHON_SOURCES = $(srcdir)/pire.pyx

MAINTAINERCLEANFILES = $(BUILT_SOURCES)

pkgpython_PYTHON =
pkgpyexec_LTLIBRARIES = pire.la
pire_la_SOURCES = $(BUILT_SOURCES) $(CYTHON_SOURCES)
pire_la_CPPFLAGS = $(PYTHON_INCLUDE) -I$(top_srcdir) $(AM_CXXFLAGS)
pire_la_LDFLAGS = -lpire -module

$(srcdir)/pire_wrap.cpp: $(CYTHON_SOURCES)
	$(CYTHON) -2 --cplus -I$(top_srcdir) -o $@ $(srcdir)/pire.pyx
