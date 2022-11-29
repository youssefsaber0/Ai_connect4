class Tree {
  constructor (){
    this.current = new Board($("#current-board"))

    this.children = []

    this.boards = [
      new Board($("#board1")),
      new Board($("#board2")),
      new Board($("#board3")),
      new Board($("#board4")),
      new Board($("#board5")),
      new Board($("#board6")),
      new Board($("#board7"))
    ]

    Object.preventExtensions();
  }


}