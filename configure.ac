AC_PREREQ([2.60])
AC_INIT([pire_py], [0.0.1], [moskupols@yandex-team.ru])
AM_INIT_AUTOMAKE([foreign -Wall])
AC_CONFIG_MACRO_DIR([m4])

AC_LANG_CPLUSPLUS
AC_PROG_CXX
AC_PROG_LIBTOOL


AM_PATH_PYTHON(2.1)
AX_PYTHON_INCLUDE
# AC_SUBST([PYTHON_INCLUDE])

AC_PATH_PROGS([CYTHON], [cython])

if ! test -r "$srcdir"/pire/pire_wrap.cpp; then
    if test x"$CYTHON" = x; then
        AC_MSG_ERROR([[Cython not found (and no pregenerated extension sources used)]])
    fi
    if ! test -r "$srcdir"/pire/pire_py.pyx || \
            ! test -r "$srcdir"/pire/impl.pxd || \
            ! test -r "$srcdir"/pire/options.h; then
        AX_PYTHON_MODULE([mako], [fatal])
    fi
fi

AC_CONFIG_FILES([
    Makefile
    pire/Makefile
    pire/tests/Makefile
    pire/tests/run-bench
    pire/tests/run-pytest
    pire/tests/run-with-pypath
], [
    chmod --silent +x \
        pire/tests/run-bench \
        pire/tests/run-pytest \
        pire/tests/run-with-pypath
])
AC_OUTPUT
