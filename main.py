from data import db_session, users, jobs


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    add_user("Scott", "Ridley", 21, "captain", "research engineer", "module_1", "scott_chief@mars.org", "cap")
    add_user('Mihalev', 'Lev', 17, 'никто', 'никто', 'module_2', 'ahah2281337@mars.org', 'pac')
    add_user('Genanany', 'Gena', 170, 'никто', 'никто', 'module_1', 'Genanany@mars.org', '123')
    add_user('Hivsys', 'Yaya', 1, 'никто', 'никто', 'module_2', 'Hivsys@mars.org', '312')
    add_job(1, 'deployment of residential modules 1 and 2', 15, '2, 3', False)
    add_job(2, 'deploрапрапрапd 2', 25, '2, 1', False)


def add_user(surname, name, age, position, speciality, address, email, hashed_password):
    session = db_session.create_session()
    user = users.User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()


def add_job(team_leader, job1, work_size, collaborators, is_finished):
    session = db_session.create_session()
    job = jobs.Job()
    job.team_leader = team_leader
    job.job = job1
    job.work_size = work_size
    job.collaborators = collaborators
    job.is_finished = is_finished
    session.add(job)
    session.commit()


if __name__ == '__main__':
    main()