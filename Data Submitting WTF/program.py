import datetime as dt

from schema import factory, User, Story, Category
from web_data import StoryForm
from flask import Flask, request, render_template, redirect


app = Flask(__name__)


@app.errorhandler(404)
def router_not_found(e):
    return render_template('page-not-found.html')


@app.route('/')
@app.route('/index')
def show_all_news():
    result = session.query(Story)
    return render_template('all-news-page.html', stories=result)


@app.route('/add-story', methods=["GET", "POST"])
def add_new_story():
    all_users = session.query(User)
    all_categories = session.query(Category)

    story_form = StoryForm()

    story_form.story_author.choices = [
        (u.id, f'{u.first_name} {u.last_name} ({u.username})') for u in all_users
    ]

    story_form.story_topics.choices = [(c.id, c.name) for c in all_categories]

    if request.method == "GET":
        story_form.creation_date.data = dt.datetime.now()
        return render_template('add-story-page.html', f=story_form)

    if request.method == "POST":
        story_form.process(request.form)

        if not story_form.validate():
            return render_template('add-story-page.html', f=story_form)

        new_story = Story()
        new_story.title = story_form.story_title.data
        new_story.content = story_form.story_content.data
        new_story.author_id = story_form.story_author.data

        if story_form.scope.data == 'public':
            new_story.is_private = False

        if story_form.creation_date.data is not None:
            new_story.created_on = story_form.creation_date.data

        print(story_form.story_topics.data)

        for category_id in story_form.story_topics.data:
            c = session.get(Category, category_id)
            new_story.categories.append(c)

        try:
            session.add(new_story)
            session.commit()
            return redirect('/index')
        except Exception as e:
            session.rollback()
            return f"Что-то пошло не так. Ошибка: {e}"


@app.route('/edit-story/<int:story_id>', methods=["GET", "POST"])
def edit_existing_story(story_id):
    story = session.get(Story, story_id)
    if story is None:
        return f"Истории с идентификатором {story_id} не существует."

    all_users = session.query(User)
    all_categories = session.query(Category)

    story_form = StoryForm()

    story_form.story_author.choices = [
        (u.id, f'{u.first_name} {u.last_name} ({u.username})') for u in all_users
    ]

    story_form.story_topics.choices = [(c.id, c.name) for c in all_categories]

    if request.method == "GET":
        story_form.story_title.data = story.title
        story_form.story_content.data = story.content
        story_form.story_author.data = story.author_id

        if story.is_private:
            story_form.scope.data = "private"
        else:
            story_form.scope.data = "public"

        story_form.story_topics.data = [c.id for c in story.categories]
        story_form.creation_date.data = story.created_on
        story_form.responsibility.data = True

        return render_template("edit-story-page.html", story_id=story.id, f=story_form)

    if request.method == "POST":
        story_form.process(request.form)

        if not story_form.validate():
            return render_template("edit-story-page.html", story_id=story.id, f=story_form)

        story.title = story_form.story_title.data
        story.content = story_form.story_content.data

        story.author_id = story_form.story_author.data

        if story_form.scope.data == 'public':
            story.is_private = False

        story.created_on = story_form.creation_date.data

        # print(story_form.story_topics.data)

        story.categories.clear()
        for category_id in story_form.story_topics.data:
            c = session.get(Category, category_id)
            story.categories.append(c)

        try:
            session.commit()
            return redirect('/index')
        except Exception as e:
            session.rollback()
            return f"Что-то пошло не так. Ошибка: {e}"


@app.route('/delete-story/<int:story_id>')
def delete_existing_story(story_id):
    story = session.get(Story, story_id)
    if story is None:
        return f"Истории с идентификатором {story_id} не существует."

    try:
        session.delete(story)
        session.commit()
        return redirect('/index')
    except Exception as e:
        session.rollback()
        return f"Что-то пошло не так. Ошибка: {e}"


if __name__ == "__main__":
    session = factory()
    app.run(host="127.0.0.1", port=4321)
