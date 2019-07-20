# test code:
# bash /Users/WilsonHuang/Downloads/nand2tetris/projects/10/testing_code.sh

# unit-testing tokenizer
#python3 /Users/WilsonHuang/Downloads/nand2tetris/projects/10/JackTokenizer.py /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square/Main.jack
#bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Main.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square/MainT.xml


# testing JackAnalyzer

## ExpressionLessSquare
python3 /Users/WilsonHuang/Downloads/nand2tetris/projects/10/JackAnalyzer.py /Users/WilsonHuang/Downloads/nand2tetris/projects/10/ExpressionLessSquare/
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Main.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/ExpressionLessSquare/Main.xml
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/SquareGame.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/ExpressionLessSquare/SquareGame.xml
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/ExpressionLessSquare/Square.xml

## ArrayTest
python3 /Users/WilsonHuang/Downloads/nand2tetris/projects/10/JackAnalyzer.py /Users/WilsonHuang/Downloads/nand2tetris/projects/10/ArrayTest/
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Main.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/ArrayTest/Main.xml

## Square
python3 /Users/WilsonHuang/Downloads/nand2tetris/projects/10/JackAnalyzer.py /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square/
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Main.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square/Main.xml
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/SquareGame.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square/SquareGame.xml
bash /Users/WilsonHuang/Downloads/nand2tetris/tools/TextComparer.sh /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square.xml /Users/WilsonHuang/Downloads/nand2tetris/projects/10/Square/Square.xml
