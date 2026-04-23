import { use, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

const champions = [
  { name: 'Aatrox' },
  { name: 'Ahri' },
  { name: 'Akali' },
  { name: 'Amumu' },
  { name: 'Anivia' }
];

const times = [
  { name: 'LOUD' },
  { name: 'FURIA' }
];



function App() {

  const[selecaoTemporaria, setSelecaoTemporaria] = useState(null)
  const[champsBloqueados, setChampsBloqueados] = useState([])
  const tratarCliqueNoChamp = (champion) => {
    setSelecaoTemporaria(champion)
  }
  const confirmarSelecao = async () => {
    if(!selecaoTemporaria) return
    setChampsBloqueados([...champsBloqueados, selecaoTemporaria.name])
    setSelecaoTemporaria(null)
  }

  const iniciarDraft = async () =>{
     const dadosDraft = {
      sessionId: "TESTE_1",
      timeAzul: timeConfirmadoBlue.name,
      timeRed: timeConfirmadoRed.name,
      formato: formatoMD,
      firstPick: ladoFirstPick
    }
    console.log("enviando para o java", dadosDraft)

    //chamar funcçao backend
  }
  
  let textoBotao = "selecione um campeao"
  let botaoDesabilitado = true
  
  if(selecaoTemporaria != null){
    textoBotao = "confirmar " + selecaoTemporaria.name
    botaoDesabilitado = false;
  }

  const [formatoMD, setFormatoMD] = useState('MD1')

  const[ladoFirstPick, setLadoFirstPick] = useState('BLUE')

  const [buscaTimeBlue, setBuscaTimeBlue] = useState('');
  const [timeEscolhidoBlue, setTimeEscolhidoBlue] = useState(null);



  const [timeTempBlue, setTimeTempBlue] = useState(null);
  const [timeConfirmadoBlue, setTimeConfirmadoBlue] = useState(null);


  const [timeTempRed, setTimeTempRed] = useState(null);
  const [timeConfirmadoRed, setTimeConfirmadoRed] = useState(null);
 
  const confirmarTimeBlue = () => {
    if (timeTempBlue != null) {
      setTimeConfirmadoBlue(timeTempBlue);
      setTimeTempBlue(null); 
    }
  };

  const confirmarTimeRed = () => {
    if (timeTempRed != null) {
      setTimeConfirmadoRed(timeTempRed);
      setTimeTempRed(null); 
    }
  };
  return (

    <div className='main-container'>
      <aside className='blue-team'>
        <h2>{timeConfirmadoBlue ? timeConfirmadoBlue.name : "Blue Side"}</h2>
        <header className='search-header'>
          <input 
          type="text" 
          placeholder='Pesquisar time...' 
          />
          
          {(timeConfirmadoBlue === null || timeConfirmadoRed=== null || timeConfirmadoBlue.name === timeConfirmadoRed.name) && (
            <div className='selecao-time-container'>
            <div className='times-lista'>
              {times.map((time) => {
                let classeTime = "time-card"
                if(timeTempBlue != null && timeTempBlue.name === time.name){
                  classeTime = "time-card selected-blue"
                }
                return (
                  <div
                  key={time.name}
                  className={classeTime}
                  onClick={() => setTimeTempBlue(time)}>
                    {time.name}
                  </div>
                )
              })}
            </div>
            <button
            className='btn-confirmar-time'
            onClick ={confirmarTimeBlue}
            disabled={timeTempBlue === null}  
              >
                Confirmar time azul
              
            </button>

          </div>
          )

          }
        </header>
        <header className="filter-header">
          <label>
            <input type="checkbox" 
            checked = {ladoFirstPick === 'BLUE'}
            onChange={() => setLadoFirstPick('BLUE')}
            /> é first pick?
          </label>
        </header>
        <div className='bans'>
          <p>champs banidos</p>
        </div>
        <div className='picks'>
          <p>picks</p>
        </div>
        
      </aside>

      <main className='champions-selection'>
        <header className="filter-header">
          <input 
          type="text" 
          placeholder='Pesquisar Liga...' 
          />
          <label>
            <input type="checkbox" checked={formatoMD === 'MD1'}
            onChange={() => setFormatoMD('MD1')} /> MD1
          </label>
          <label>
            <input type="checkbox" checked={formatoMD === 'MD3'}
            onChange={() => setFormatoMD('MD3')} /> MD3
          </label>
          <label>
            <input type="checkbox" checked={formatoMD === 'MD5'}
            onChange={() => setFormatoMD('MD5')} /> MD5
          </label>
          {(timeConfirmadoBlue !== null && timeConfirmadoRed !== null && timeConfirmadoBlue.name !== timeConfirmadoRed.name) && (
            <button className='bn-iniciar-draft'
            onClick={iniciarDraft}>
              iniciarDraft
            </button>
          )}
        </header>
        <p>champs banidos pelo fearless</p>
        <h2>Picks e Bans</h2>
        <header className='search-header'>
          <input 
          type="text" 
          placeholder='Pesquisar campeao...' 
          />
          <div className='confirm-area'>
            <button
            className='btn-confirmar'
            onClick={confirmarSelecao}
            disabled={botaoDesabilitado}>
              {textoBotao}
            </button>
          </div>
        </header>
        <header className="filter-header">
          <input type="checkbox" id="top" name="position" />Top
          <input type="checkbox" id="Jungle" name="position" />Jungle
          <input type="checkbox" id="Mid" name="position" />Mid
          <input type="checkbox" id="Adc" name="position" />Adc
          <input type="checkbox" id="Sup" name="position" />Sup
        </header>

        <p>lista de champs</p>
        <div className='champions-grid'>
          {champions.map((champion) => {
            const foiConfirmado = champsBloqueados.includes(champion.name)
            let estaSelecionadoAgora = false
            if(selecaoTemporaria != null){
              if(selecaoTemporaria.name === champion.name){
                estaSelecionadoAgora = true
              }
            }
            let classeFinal = "champion-card"
            if(foiConfirmado){
              classeFinal = "champion-card disabled"
            } else if(estaSelecionadoAgora){
              classeFinal = "champion-card selected"
            }
            const clicarNoChamp = () => {
              if(foiConfirmado === false){
                tratarCliqueNoChamp(champion)
              }
            }
            return (
              <div
              key={champion.name}
              className={classeFinal}
              onClick={clicarNoChamp}
              >
                {champion.name}
              </div>
            )
          })}
        </div>
        
      </main>

      <aside className='red-team'>
        <h2> {timeConfirmadoRed ? timeConfirmadoRed.name : "Red Side"} </h2>
        <header className='search-header'>
          <input 
          type="text" 
          placeholder='Pesquisar time...' 
          />
          {(timeConfirmadoBlue === null || timeConfirmadoRed=== null || timeConfirmadoBlue.name === timeConfirmadoRed.name) && (
            <div className='selecao-time-container'>
            <div className='times-lista'>
              {times.map((time) => {
                let classeTime = "time-card"
                if(timeTempRed != null && timeTempRed.name === time.name){
                  classeTime = "time-card selected-red"
                }
                return (
                  <div
                  key={time.name}
                  className={classeTime}
                  onClick={() => setTimeTempRed(time)}>
                    {time.name}
                  </div>
                )
              })}
            </div>

            <button
            className='btn-confirmar-time'
            onClick ={confirmarTimeRed}
            disabled={timeTempRed === null}  
              >
                Confirmar time vermelho
              
            </button>
          </div>

          )}
          

        </header>
        <header className="filter-header">
          <label>
            <input type="checkbox" 
            checked = {ladoFirstPick === 'RED'}
            onChange={() => setLadoFirstPick('RED')}
            /> é first pick?
          </label>
        </header>
         <div className='bans'>
          <p>champs banidos</p>
        </div>
        <div className='picks'>
          <p>picks</p>
        </div>
        
      </aside>
    </div>
    
  )
}

export default App
