#pragma once
#ifndef COMPATIBILITY
   #define   COMPATIBILITY 

   #define fscanf_s                         fscanf
   #define sscanf_s                         sscanf
   #define scanf_s                          scanf
   #define printf_s                         printf
   #define sprintf_s                        sprintf
   #define fprintf_s                        fprintf
   #define strcpy_s(dest, count, source)    strncpy( (dest), (source), (count) )
   #define fopen_s(fp, fmt, mode)          *(fp)=fopen( (fmt), (mode))
   #define _fcloseall                       fcloseall
   #define strtok_s                         strtok
   #define _strcmpi                         strcmpi
   #define strncpy_s                        strncpy
   #define errno_t                          int
   #define _strdup                          strdup

#endif // COMPATIBILITY