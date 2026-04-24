const BASE_URL = 'http://localhost:8080'

let sessionIdGlobal = null;
export const draftService = {
    iniciarDraft: async (dados) => {
        const resposta = await fetch (`${BASE_URL}/draft/Start`,{
             method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
        })
        const dadosResposta = await resposta.json();
        sessionIdGlobal = dadosResposta.sessionId
        return dadosResposta;
    },

    getSessionId: () => sessionIdGlobal
}