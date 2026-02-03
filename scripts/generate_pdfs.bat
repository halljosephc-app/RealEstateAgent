@echo off
REM Generate PDFs from markdown files in the output folder
REM Usage: generate_pdfs.bat [output_folder]
REM   If no folder specified, uses current directory

setlocal

if "%~1"=="" (
    set OUTPUT_DIR=%CD%
) else (
    set OUTPUT_DIR=%~1
)

echo.
echo Generating PDFs from markdown files in: %OUTPUT_DIR%
echo.

cd /d "%OUTPUT_DIR%"

for %%f in (*.md) do (
    echo Converting: %%f
    call npx md-to-pdf "%%f"
)

echo.
echo Done! PDFs generated in: %OUTPUT_DIR%
echo.

endlocal
