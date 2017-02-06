AC_DEFUN([AX_PYTHON_INCLUDE], [
	AM_PATH_PYTHON
	AC_ARG_VAR([PYTHON_INCLUDE], [Path to directory with python headers])
	AC_ARG_VAR([PYTHON_CONFIG], [Path to python-config])

	AS_IF([test -z "$PYTHON_INCLUDE"], [
		AS_IF([test -z "$PYTHON_CONFIG"], [
			AC_PATH_PROGS(
				[PYTHON_CONFIG],
				[python$PYTHON_VERSION-config python-config],
				[no]
			)
			AS_IF([test x"$PYTHON_CONFIG" = xno], [
				AC_MSG_ERROR([cannot find python-config for $PYTHON.])
			])
		])
		AC_MSG_CHECKING([python include flags])
		PYTHON_INCLUDE=`$PYTHON_CONFIG --includes`
		AC_SUBST([PYTHON_INCLUDE])
		AC_MSG_RESULT([$PYTHON_INCLUDE])
	])
])
