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

if ! test -r "$srcdir"/bindings/python/pire_wrap.cpp && test x"$CYTHON" = x; then
    AC_MSG_ERROR([[Cython not found (and no prebuilt python wrapper used)]])
fi

# Just for conscience' sake
AC_CONFIG_FILES([
	Makefile
	pire/Makefile
])
AC_OUTPUT
