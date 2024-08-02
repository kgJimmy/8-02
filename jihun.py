import requests
import hgtk
import random

# 이미 있는 단어 알기 위해 단어 목록 저장
history = []
playing = True

# 키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
apikey = '2D319D85D76F61B0923A0A127E2AAB4E'

# 좀 치사한 한방 단어 방지 목록
blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍', '튼', '름', '늠', '쁨']

# 지정한 두 개의 문자열 사이의 문자열을 리턴하는 함수
def midReturn(val, s, e):
    if s in val:
        val = val[val.find(s)+len(s):]
        if e in val:
            val = val[:val.find(e)]
    return val

# 지정한 두 개의 문자열 사이의 문자열 여러 개를 리턴하는 함수
def midReturn_all(val, s, e):
    if s in val:
        tmp = val.split(s)
        val = [x[:x.find(e)] for x in tmp if e in x]
    else:
        val = []
    return val

def findword(query):
    url = f'https://krdict.korean.go.kr/api/search?key={apikey}&part=word&pos=1&q={query}'
    response = requests.get(url)
    ans = []

    # 단어 목록을 불러오기
    words = midReturn_all(response.text, '<item>', '</item>')
    for w in words:
        # 이미 쓴 단어가 아닐 때
        if w not in history:
            # 한글자가 아니고 품사가 명사일 때
            word = midReturn(w, '<word>', '</word>')
            pos = midReturn(w, '<pos>', '</pos>')
            if len(word) > 1 and pos == '명사' and word[len(word)-1] not in blacklist:
                ans.append(w)
    if ans:
        return random.choice(ans)
    else:
        return ''

def checkexists(query):
    if len(query) != 3:
        return ''
    url = f'https://krdict.korean.go.kr/api/search?key={apikey}&part=word&sort=popular&num=100&pos=1&q={query}'
    response = requests.get(url)
    ans = ''

    # 단어 목록을 불러오기
    words = midReturn_all(response.text, '<item>', '</item>')
    for w in words:
        # 이미 쓴 단어가 아닐 때
        if w not in history:
            # 한글자가 아니고 품사가 명사일 때
            word = midReturn(w, '<word>', '</word>')
            pos = midReturn(w, '<pos>', '</pos>')
            if len(word) > 1 and pos == '명사' and word == query:
                ans = w

    return ans

def provide_hint(start):
    hint = findword(start + '*')
    
    if hint:
        return f"힌트: '{midReturn(hint, '<word>', '</word>')}'"
    return "힌트가 없습니다."

print(''')
=============파이썬 끝말잇기===============
사전 데이터 제공: 국립국어원 한국어기초사전
- - - 게임 방법 - - -
가장 처음 단어를 제시하면 끝말잇기가 시작됩니다
'/그만'을 입력하면 게임이 종료되며, '/다시'를 입력하여 게임을 다시 시작할 수 있습니다.
- - - 게임 규칙 - - -
1. 사전에 등재된 명사여야 합니다
2. 적어도 단어의 길이가 두 글자 이상이어야 합니다
3. 이미 사용한 단어를 다시 사용할 수 없습니다
4. 두음법칙 적용 가능합니다 (ex. 리->니)
==========================================
''')

answord = ''
sword = ''

while playing:
    wordOK = False

    while not wordOK:
        query = input(answord + ' > ')
        wordOK = True
        
        if query == '/그만':
            playing = False
            print('컴퓨터의 승리!')
            break
        elif query == '/다시':
            history = []
            answord = ''
            print('게임을 다시 시작합니다.')       
            wordOK = False
        else:
            if query == '':
                wordOK = False
                if not history:
                    print('단어를 입력하여 끝말잇기를 시작합니다.')
                else:
                    print(sword + '(으)로 시작하는 단어를 입력해 주십시오.')
            else:
                # 첫 글자의 초성 분석하여 두음법칙 적용
                if not len(history) == 0 and not query[0] == sword and query:
                    sdis = hgtk.letter.decompose(sword)
                    qdis = hgtk.letter.decompose(query[0])
                    if sdis[0] == 'ㄹ' and qdis[0] == 'ㄴ':
                        print('두음법칙 적용됨')
                    elif (sdis[0] == 'ㄹ' or sdis[0] == 'ㄴ') and qdis[0] == 'ㅇ' and qdis[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'):
                        print('두음법칙 적용됨')
                    else:
                        wordOK = False
                        print(sword + '(으)로 시작하는 단어여야 합니다.')

                if len(query) == 2:
                    wordOK = False
                    print('적어도 세 글자가 되어야 합니다')

                if query in history:
                    wordOK = False
                    print('이미 입력한 단어입니다')

                if query[len(query)-1] in blacklist:
                    print('아.. 좀 치사한데요..')

                if wordOK:
                    # 단어의 유효성을 체크
                    ans = checkexists(query)
                    if ans == '':
                        wordOK = False
                        print('유효한 단어를 입력해 주십시오')
                    else:
                        print('(' + midReturn(ans, '<definition>', '</definition>') + ')\n')
                        
    history.append(query)
    
    if playing:
        start = query[len(query)-1]
        ans = findword(start + '*')

        if ans == '':
            # ㄹ -> ㄴ 검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄹ':
                newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
                print(start, '->', newq)
                start = newq
                ans = findword(newq + '*')

        if ans == '':
            # (ㄹ->)ㄴ -> ㅇ 검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄴ' and sdis[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'):
                newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
                print(start, '->', newq)
                ans = findword(newq + '*')
        
        if ans == '':
            print('당신의 승리!')
            break
        else:
            answord = midReturn(ans, '<word>', '</word>')  # 단어 불러오기
            ansdef = midReturn(ans, '<definition>', '</definition>')  # 정의 불러오기
            history.append(answord)
            
            print(query, '>', answord, '\n(' + ansdef + ')\n')
            sword = answord[len(answord)-1]

            # 힌트 제공
            hint = provide_hint(sword)
            if hint:
                print(hint)
