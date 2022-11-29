class Board {
  PLAYER = "red"
  BOT = "yellow"

  constructor(wrapper) {
    this.container = wrapper
    this.turn = this.PLAYER
    this.state = "6666666"

    this.__initBoard()
    this.cell_border
    this.cell_height

    Object.preventExtensions()
  }

  __initBoard() {
    this.show()
    this.showTurn()
    $("#score1").html(0)
    $("#score2").html(0)

    for (let col = 0; col < 7; col++) {
      $(this.container).append(`
        <div class="col" col="${col}"></div>
      `);
      for (let row = 0; row < 6; row++) {
        if(row == 0){
          $(this.container).find("[col=" + col + "]").append(`
            <div class="slot">
              <div class="slot-fill"></div>
            </div>
          `)

          this.cell_border = parseInt(this.$(".slot").eq(0).css("border").split("px")[0])
          this.cell_height = this.$(".slot").eq(0).height() + this.cell_border * 2

          $(this.container).find("[col=" + col + "] .slot .slot-fill").css("top", `-${this.cell_height}px;`)

          continue;
        }

        $(this.container).find("[col=" + col + "]").append(`
          <div class="slot">
            <div class="slot-fill" style="top:-${this.cell_height}px;"></div>
          </div>
        `)
      }
    }
  }

  $(selector) {
    return $(this.container).find(selector)
  }

  showTurn(turn=null) {
    if(turn)
      this.turn = turn   

    $("#turn").html(this.turn + "'s turn").css("color", `var(--${this.turn})`)
  }

  __toggleTurn() {
    this.showTurn(this.turn == this.PLAYER ? this.BOT : this.PLAYER)
  }

  drop(col) {
    if(this.state[col] == 0)
      throw new ColumnOverflow;

    // Drop piece
    let slot = this.$(`[col=${col}] .slot:nth-child(${parseInt(this.state[col])}) .slot-fill`)
    $(slot).addClass(`${this.turn}-slot`)
    $(slot).css("top", this.cell_border + this.cell_height * (this.state[col] - 1))

    // Update state
    this.state = this.state.replaceAt(col, this.state[col] - 1)
    this.__toggleTurn()
  }

  undo(col) {
    if(this.state[col] == 0)
      throw new ColumnUnderflow;

    // Update state
    this.__toggleTurn()
    this.state = this.state.replaceAt(col, this.state[col] + 1)

    // Remove piece
    let slot = this.$(`[col=${col}] .slot:nth-child(${parseInt(this.state[col])}) .slot-fill`)
    $(slot).removeClass(`${this.turn}-slot`)
    $(slot).css("top", this.cell_border + this.cell_height * (this.state[col] - 1))
  }

  hide() {
    $(this.container).css("opacity", "0")
  }

  show() {
    $(this.container).css("opacity", "")
  }
}

class ColumnOverflow extends Error {
  constructor(){
    super("Column is filled")
    this.name = "ColumnOverflow"
  }
}

class ColumnUnderflow extends Error {
  constructor(){
    super("Column is filled")
    this.name = "ColumnOverflow"
  }
}