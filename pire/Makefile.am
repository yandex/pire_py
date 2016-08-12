SUBDIRS = . tests

RENDER_PY = $(srcdir)/render.py

MAKO_SOURCES = $(srcdir)/pire_py.pyx.mako $(srcdir)/impl.pxd.mako $(srcdir)/options.h.mako
CYTHON_SOURCES = $(srcdir)/pire_py.pyx $(srcdir)/impl.pxd $(srcdir)/stub.pxd
CXX_SOURCES = $(srcdir)/pire_wrap.cpp $(srcdir)/options.h

MAINTAINERCLEANFILES = $(CXX_SOURCES) pire_wrap.h $(CYTHON_SOURCES)

pkgpython_PYTHON =
pkgpyexec_LTLIBRARIES = pire_py.la
pire_py_la_SOURCES = $(CXX_SOURCES) $(CYTHON_SOURCES) $(MAKO_SOURCES) $(RENDER_PY)
pire_py_la_CPPFLAGS = $(PYTHON_INCLUDE) -I$(top_srcdir) $(AM_CXXFLAGS)
pire_py_la_LDFLAGS = -lpire -module

%.pyx: %.pyx.mako $(RENDER_PY)
	$(PYTHON) $(RENDER_PY) -i $< -o $@
%.pxd: %.pxd.mako $(RENDER_PY)
	$(PYTHON) $(RENDER_PY) -i $< -o $@
$(srcdir)/options.h: options.h.mako $(RENDER_PY)
	$(PYTHON) $(RENDER_PY) -i $< -o $@

CYTHONFLAGS=

$(srcdir)/pire_wrap.cpp: $(CYTHON_SOURCES) $(srcdir)/options.h
	$(CYTHON) -2 --cplus $(CYTHONFLAGS) -I$(top_srcdir) -o $@ $(srcdir)/pire_py.pyx
